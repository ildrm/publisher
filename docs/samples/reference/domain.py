"""Immutable structured manuscript, permissions, and in-memory save contract."""
from dataclasses import dataclass
from hashlib import sha256
from threading import Lock
import json


class ValidationError(ValueError):
    pass


class AccessDenied(PermissionError):
    pass


class ConflictError(RuntimeError):
    pass


@dataclass(frozen=True)
class Node:
    kind: str
    text: str = ""
    children: tuple["Node", ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.children, tuple) or not all(isinstance(n, Node) for n in self.children):
            raise ValidationError("children must be an immutable tuple of nodes")
        allowed = {"chapter": {"heading", "paragraph"}, "heading": set(), "paragraph": set()}
        if self.kind not in allowed or any(child.kind not in allowed[self.kind] for child in self.children):
            raise ValidationError("invalid node or nesting")
        if not isinstance(self.text, str) or (self.kind == "chapter" and self.text):
            raise ValidationError("invalid text")
        if self.kind != "chapter" and (not self.text.strip() or len(self.text) > 10_000):
            raise ValidationError("text must be nonempty and within limit")
        if self.kind == "chapter" and (not self.children or len(self.children) > 1_000):
            raise ValidationError("chapter must have 1–1000 blocks")


@dataclass(frozen=True)
class Chapter:
    chapter_id: str
    root: Node

    def __post_init__(self) -> None:
        if not self.chapter_id or self.root.kind != "chapter":
            raise ValidationError("chapter ID and chapter root required")


@dataclass(frozen=True)
class Project:
    tenant_id: str
    project_id: str
    chapters: tuple[Chapter, ...]

    def __post_init__(self) -> None:
        if not self.tenant_id or not self.project_id or not isinstance(self.chapters, tuple):
            raise ValidationError("project scope and immutable chapters required")
        if not all(isinstance(c, Chapter) for c in self.chapters) or not self.chapters:
            raise ValidationError("at least one valid chapter required")
        ids = [c.chapter_id for c in self.chapters]
        if len(ids) != len(set(ids)):
            raise ValidationError("chapter IDs must be unique")


@dataclass(frozen=True)
class SaveResult:
    revision: int
    project: Project


def _fingerprint(project: Project, expected: int, actor: str) -> str:
    from dataclasses import asdict
    payload = json.dumps([actor, expected, asdict(project)], sort_keys=True, ensure_ascii=False).encode()
    return sha256(payload).hexdigest()


class SaveStore:
    """Process-local simulation; lock is not a distributed transaction or durable storage."""
    def __init__(self, initial: Project, writers: set[str]):
        self._lock = Lock()
        self._current = SaveResult(0, initial)
        self._writers = set(writers)
        self._requests: dict[str, tuple[str, SaveResult]] = {}

    def revoke(self, actor: str) -> None:
        with self._lock:
            self._writers.discard(actor)

    def save(self, actor: str, project: Project, expected: int, operation_key: str) -> SaveResult:
        if not operation_key:
            raise ValidationError("operation key required")
        with self._lock:
            if actor not in self._writers or (project.tenant_id, project.project_id) != (self._current.project.tenant_id, self._current.project.project_id):
                raise AccessDenied("not authorized")
            fingerprint = _fingerprint(project, expected, actor)
            previous = self._requests.get(operation_key)
            if previous:
                if previous[0] != fingerprint:
                    raise ConflictError("operation key reused with different input")
                return previous[1]
            if expected != self._current.revision:
                raise ConflictError("stale revision; manual recovery required")
            result = SaveResult(expected + 1, project)
            self._current = result
            self._requests[operation_key] = (fingerprint, result)
            return result

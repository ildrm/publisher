"""In-memory authorization, job deduplication and atomic promotion illustration."""
from dataclasses import dataclass
from hashlib import sha256
from threading import Lock
import json
from collections.abc import Callable


@dataclass(frozen=True)
class Artifact:
    content: bytes
    checksum: str


class ExportWorker:
    def __init__(self, grants: set[tuple[str, str]]) -> None:
        self._lock = Lock()
        self._grants = set(grants)  # (actor, target), illustrative scoped authorization
        self._jobs: dict[str, tuple[str, Artifact]] = {}
        self._good: dict[str, Artifact] = {}

    def revoke(self, actor: str, target: str) -> None:
        with self._lock:
            self._grants.discard((actor, target))

    def run(self, actor: str, job_key: str, target: str, source: bytes, profile: str,
            convert: Callable[[bytes], bytes]) -> Artifact:
        if not actor or not job_key or not target or not profile or not isinstance(source, bytes):
            raise ValueError("actor, job key, target, profile and bytes required")
        fingerprint = sha256(json.dumps([target, profile, sha256(source).hexdigest()], ensure_ascii=False).encode()).hexdigest()
        with self._lock:
            # Authorization is current even when an existing job result is available.
            if (actor, target) not in self._grants:
                raise PermissionError("not authorized")
            if job_key in self._jobs:
                prior_fingerprint, prior = self._jobs[job_key]
                if prior_fingerprint != fingerprint:
                    raise ValueError("job key reused with different input")
                return prior
            # Lock only models atomic promotion in one process; production uses a transaction.
            output = convert(source)
            if not isinstance(output, bytes) or not output:
                raise ValueError("conversion produced no artifact")
            artifact = Artifact(output, sha256(output).hexdigest())
            self._jobs[job_key] = (fingerprint, artifact)
            self._good[target] = artifact
            return artifact

    def good(self, actor: str, target: str) -> Artifact | None:
        with self._lock:
            if (actor, target) not in self._grants:
                raise PermissionError("not authorized")
            return self._good.get(target)

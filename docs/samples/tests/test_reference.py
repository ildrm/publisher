import hmac
import json
from hashlib import sha256
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from reference.domain import AccessDenied, Chapter, ConflictError, Node, Project, SaveStore, ValidationError
from reference.export import ExportWorker
from reference.finance import Entry, Ledger, WebhookReceiver
from reference.upload import UploadPolicy, inspect_upload


def project(text="hello", tenant="tenant-a"):
    return Project(tenant, "project-a", (Chapter("c1", Node("chapter", children=(Node("paragraph", text),))),))


def docx(extra=None):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", "<document/>")
        if extra:
            z.writestr(*extra)
    return buffer.getvalue()


class DomainTests(unittest.TestCase):
    def test_reject_invalid_nesting_and_mutable_children(self):
        with self.assertRaises(ValidationError):
            Node("paragraph", "x", (Node("heading", "h"),))
        with self.assertRaises(ValidationError):
            Node("chapter", children=[Node("paragraph", "x")])

    def test_duplicate_chapters_rejected(self):
        chapter = project().chapters[0]
        with self.assertRaises(ValidationError):
            Project("t", "p", (chapter, chapter))

    def test_lost_response_retry_is_idempotent(self):
        store = SaveStore(project(), {"alice"})
        result = store.save("alice", project("new"), 0, "key-1")
        self.assertEqual(store.save("alice", project("new"), 0, "key-1"), result)
        self.assertEqual(result.revision, 1)

    def test_stale_write_and_key_reuse_are_rejected(self):
        store = SaveStore(project(), {"alice"})
        store.save("alice", project("one"), 0, "k")
        with self.assertRaises(ConflictError):
            store.save("alice", project("two"), 0, "other")
        with self.assertRaises(ConflictError):
            store.save("alice", project("different"), 0, "k")

    def test_concurrent_same_version_has_one_winner(self):
        store = SaveStore(project(), {"alice"})
        barrier = Barrier(2)
        def attempt(text):
            barrier.wait()
            try:
                return store.save("alice", project(text), 0, text).revision
            except ConflictError:
                return "conflict"
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(attempt, ("one", "two")))
        self.assertCountEqual(results, [1, "conflict"])

    def test_scope_and_revocation_checked_even_on_retry(self):
        store = SaveStore(project(), {"alice"})
        with self.assertRaises(AccessDenied):
            store.save("alice", project(tenant="tenant-b"), 0, "k")
        store.save("alice", project("one"), 0, "k")
        store.revoke("alice")
        with self.assertRaises(AccessDenied):
            store.save("alice", project("one"), 0, "k")


class ExportTests(unittest.TestCase):
    def test_duplicate_checks_current_grant_before_returning_artifact(self):
        worker = ExportWorker({("alice", "target"), ("bob", "target")})
        first = worker.run("alice", "a", "target", b"source", "v1", lambda source: source.upper())
        second = worker.run("bob", "a", "target", b"source", "v1", lambda _: self.fail("must not run"))
        self.assertEqual(first, second)
        self.assertEqual(first.checksum, sha256(b"SOURCE").hexdigest())
        worker.revoke("alice", "target")
        with self.assertRaises(PermissionError):
            worker.run("alice", "a", "target", b"source", "v1", lambda _: b"x")
        with self.assertRaises(PermissionError):
            worker.good("alice", "target")

    def test_failure_preserves_good_and_same_key_can_retry(self):
        worker = ExportWorker({("alice", "target")})
        good = worker.run("alice", "a", "target", b"source", "v1", lambda _: b"good")
        with self.assertRaises(RuntimeError):
            worker.run("alice", "b", "target", b"new", "v1", lambda _: (_ for _ in ()).throw(RuntimeError("failure")))
        self.assertEqual(worker.good("alice", "target"), good)
        retried = worker.run("alice", "b", "target", b"new", "v1", lambda _: b"new-good")
        self.assertEqual(retried.content, b"new-good")
        with self.assertRaises(ValueError):
            worker.run("alice", "a", "target", b"source", "v2", lambda _: b"bad")


class FinanceTests(unittest.TestCase):
    def test_webhook_signs_raw_body_and_deduplicates(self):
        receiver = WebhookReceiver(b"key", "acct-a")
        raw = b'{"id":"e1","type":"payment.confirmed","account":"acct-a"}'
        sign = lambda body, ts: hmac.new(b"key", str(ts).encode() + b"." + body, sha256).hexdigest()
        self.assertEqual(receiver.receive(raw, 1000, sign(raw, 1000), 1000), "accepted")
        self.assertEqual(receiver.receive(raw, 1000, sign(raw, 1000), 1100), "duplicate")
        with self.assertRaises(PermissionError):
            receiver.receive(raw + b" ", 1000, sign(raw, 1000), 1000)
        with self.assertRaises(PermissionError):
            receiver.receive(raw, 1000, sign(raw, 1000), 1301)
        changed = json.dumps({"id": "e1", "type": "payment.confirmed", "account": "acct-a", "extra": 1}).encode()
        with self.assertRaises(ValueError):
            receiver.receive(changed, 1001, sign(changed, 1001), 1001)

    def test_webhook_rejects_wrong_account_and_event_with_valid_signature(self):
        receiver = WebhookReceiver(b"key", "acct-a")
        for raw in (b'{"id":"e1","type":"payment.pending","account":"acct-a"}',
                    b'{"id":"e1","type":"payment.confirmed","account":"acct-b"}'):
            sig = hmac.new(b"key", b"1000." + raw, sha256).hexdigest()
            with self.assertRaises(ValueError):
                receiver.receive(raw, 1000, sig, 1000)

    def test_balanced_accrual_and_payout_retry(self):
        ledger = Ledger("USD")
        entries = (Entry("expense", debit=3000), Entry("royalty_payable", credit=3000))
        ledger.post("accrual", entries)
        ledger.post("accrual", entries)
        self.assertEqual(ledger.payable(), 3000)
        ledger.payout("p1", 3000, cleared=3000)
        ledger.payout("p1", 3000, cleared=0)
        self.assertEqual(ledger.payable(), 0)

    def test_unbalanced_key_collision_and_payout_limits(self):
        ledger = Ledger("USD")
        with self.assertRaises(ValueError):
            ledger.post("bad", (Entry("expense", debit=2), Entry("payable", credit=1)))
        ledger.post("r", (Entry("expense", debit=3000), Entry("royalty_payable", credit=3000)))
        with self.assertRaises(ValueError):
            ledger.payout("p", 3001, cleared=5000)
        with self.assertRaises(ValueError):
            ledger.payout("p", 2000, cleared=1000)
        with self.assertRaises(ValueError):
            ledger.post("r", (Entry("expense", debit=1), Entry("royalty_payable", credit=1)))


class UploadTests(unittest.TestCase):
    def test_supported_markdown_and_minimal_docx(self):
        self.assertEqual(inspect_upload("a.md", "سلام".encode()), "markdown")
        self.assertEqual(inspect_upload("a.docx", docx()), "docx")

    def test_reject_type_spoof_and_path_traversal(self):
        with self.assertRaises(ValueError):
            inspect_upload("a.docx", b"not a zip")
        with self.assertRaises(ValueError):
            inspect_upload("a.docx", docx(("../escape", "x")))

    def test_reject_decompression_limits_and_active_content(self):
        with self.assertRaises(ValueError):
            inspect_upload("a.docx", docx(("huge.txt", "a" * 10000)), UploadPolicy(max_ratio=2))
        with self.assertRaises(ValueError):
            inspect_upload("a.docx", docx(("word/vbaProject.bin", b"macro")))

    def test_reject_unsafe_xml_and_oversize(self):
        with self.assertRaises(ValueError):
            inspect_upload("a.docx", docx(("custom.xml", '<!DOCTYPE x [<!ENTITY a "x">]>')))
        with self.assertRaises(ValueError):
            inspect_upload("a.md", b"x" * 11, UploadPolicy(max_bytes=10))


if __name__ == "__main__":
    unittest.main()

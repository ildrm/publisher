"""Illustrative authenticated event intake and balanced integer-unit ledger."""
from dataclasses import dataclass
from hashlib import sha256
from threading import Lock
import hmac
import json


class WebhookReceiver:
    def __init__(self, secret: bytes, account: str, window_seconds: int = 300) -> None:
        if not secret or not account or type(window_seconds) is not int or window_seconds <= 0:
            raise ValueError("secret required")
        self._secret = secret
        self._account = account
        self._window_seconds = window_seconds
        self._seen: dict[str, bytes] = {}
        self._lock = Lock()

    def receive(self, raw: bytes, timestamp: int, signature: str, now: int) -> str:
        if not isinstance(raw, bytes) or not isinstance(signature, str) or not signature.isascii() or type(timestamp) is not int or type(now) is not int:
            raise PermissionError("invalid signature")
        if abs(now - timestamp) > self._window_seconds:
            raise PermissionError("stale signature")
        signed = str(timestamp).encode("ascii") + b"." + raw
        expected = hmac.new(self._secret, signed, sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise PermissionError("invalid signature")
        try:
            event = json.loads(raw)
            event_id = event["id"]
            if not isinstance(event_id, str) or not event_id or event["type"] != "payment.confirmed" or event["account"] != self._account:
                raise ValueError("invalid event")
        except (ValueError, KeyError, TypeError, UnicodeDecodeError) as exc:
            raise ValueError("invalid event") from exc
        digest = sha256(raw).digest()
        with self._lock:
            if event_id in self._seen:
                if self._seen[event_id] != digest:
                    raise ValueError("event ID reused with different body")
                return "duplicate"
            self._seen[event_id] = digest
            return "accepted"


@dataclass(frozen=True)
class Entry:
    account: str
    debit: int = 0
    credit: int = 0


class Ledger:
    """One currency; caller supplies authorized, verified events and settlement state."""
    def __init__(self, currency: str) -> None:
        if not currency or not currency.isascii() or not currency.isupper() or len(currency) != 3:
            raise ValueError("three-letter currency required")
        self.currency = currency
        self._transactions: dict[str, tuple[Entry, ...]] = {}
        self._lock = Lock()

    def _post(self, key: str, entries: tuple[Entry, ...]) -> None:
        if not key or not entries or any(not e.account or type(e.debit) is not int or type(e.credit) is not int or min(e.debit, e.credit) < 0 or (e.debit == 0) == (e.credit == 0) for e in entries):
            raise ValueError("invalid entries")
        if sum(e.debit for e in entries) != sum(e.credit for e in entries):
            raise ValueError("unbalanced transaction")
        prior = self._transactions.get(key)
        if prior is not None:
            if prior != entries:
                raise ValueError("key reused with different entries")
            return
        self._transactions[key] = entries

    def post(self, key: str, entries: tuple[Entry, ...]) -> None:
        with self._lock:
            self._post(key, entries)

    def payable(self) -> int:
        with self._lock:
            return self._payable()

    def _payable(self) -> int:
        return sum(e.credit - e.debit for tx in self._transactions.values() for e in tx if e.account == "royalty_payable")

    def payout(self, key: str, amount: int, cleared: int) -> None:
        if type(amount) is not int or type(cleared) is not int or amount <= 0 or cleared < 0:
            raise ValueError("invalid amount")
        entries = (Entry("royalty_payable", debit=amount), Entry("cash", credit=amount))
        with self._lock:
            # Duplicate first: retry must succeed even if remaining payable has changed.
            prior = self._transactions.get(key)
            if prior is not None:
                self._post(key, entries)
                return
            if amount > min(cleared, self._payable()):
                raise ValueError("payout exceeds cleared payable")
            self._post(key, entries)

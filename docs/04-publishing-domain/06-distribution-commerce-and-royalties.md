# PUB-006 — Distribution, commerce and royalties

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Finance / Royalty Accounting Specialist; **consulted:** Commerce, Legal, Editorial, Security, QA; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; curated single-imprint pilot, portable drafting, rights and jurisdiction unresolved. **Related requirements:** FR-CAT-001, FR-COM-001, FR-FIN-001, FR-PUB-002.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied master prompt v1.0 §§3, 5, 11–15.

## Distribution and access

The pilot proposes a limited direct digital storefront. A catalog listing is a public description; a product specifies edition, format, price, channel and territory; an order captures customer intent; a verified payment enables an entitlement governed by terms. The publisher may later send approved, versioned artifacts and metadata to external channels via adapters; availability, fees, supported formats, settlement feeds, take-down and territory controls must be confirmed with each partner. A reliable delivery job records attempt and external acknowledgement, reconciles discrepancies and handles stale listings. No external partner is presumed available.

A user initiates checkout with a unique command key. The server creates one order, delegates payment data to the selected provider and verifies callbacks/signatures, amount, currency and event identity. An unknown outcome stays pending and is reconciled before another charge; a verified successful payment and allowed product scope produce one entitlement. Failed, duplicate, delayed, out-of-order, refund and chargeback events are handled idempotently, with any state conflict escalated. Customer access on refund or takedown follows explicit law/contract-reviewed policy rather than automatic assumptions.

## Ledger and royalty posting

The authoritative ledger has balanced debit/credit entries in a specified currency, immutable source references and an idempotent source-event key; corrections are linked compensating entries. Revenue recognition, taxes, fees, royalty base, reserves and FX are jurisdiction/contract decisions for a qualified accountant. Each contractual royalty rule identifies beneficiary, edition/format/channel/territory, calculation base, rate, period, advances or caps if applicable, effective interval and evidence version. A transaction can be earned but not cleared/payable. A payout requires approved beneficiary, reconciled cleared balance, rights/dispute checks, separation of duties and unique payout key. A failed payout preserves liability and enters a retry/reconciliation queue; payment provider and bank reports are independently matched.

**Illustrative accounting only, not a pricing or tax proposal:** a settled eligible sale creates a balanced posting for the applicable proceeds and liabilities under the chosen accounting policy; the royalty calculation generates an attributable royalty payable and offsetting expense or contractual allocation. A refund creates a linked reversal or adjustment under the approved rule. Replayed sale or refund events cannot produce a second posting. Before a transfer, finance compares cleared payable, holds and previous payouts; the requested amount cannot exceed the approved cleared balance. Journal-account mapping and numerical calculation await OQ-009 and accountant approval.

| State / control | Required evidence |
|---|---|
| Payment pending → confirmed / failed / disputed | Verified provider event, amount/currency and order match; duplicate detection. |
| Refund requested → approved/denied → settled | Authorized reason, provider confirmation, compensating ledger record and support notification. |
| Royalty calculated → reviewed → payable | Rule version, source sale, calculation inputs, currency, holds and balanced entries. |
| Payout eligible → initiated → paid / failed / disputed | Cleared balance, independent approval, idempotency key and external settlement reconciliation. |

No real sale, contract, tax treatment, refund policy, vendor capability or payout was tested. Finance and legal owners must approve policies and run replay, refund, chargeback and payout reconciliation exercises before paid operation.

## Illustrative balanced journal and replay control

The following is a synthetic calculation, not tax advice or an approved accounting policy. Assume one 100.00-unit sale in one currency, no tax, fees, reserve or FX, 30% royalty on gross receipts, no advance, the retailer owes the full amount, and accounting policy treats the royalty as expense. The numbers are examples only; Finance must approve account mapping, royalty basis, rounding, recognition and settlement treatment before live operation. Each row pair balances independently and stores order, contract/rule version, currency, unique source-event key and transaction ID.

| Event and unique key | Debit | Credit | Result |
|---|---:|---:|---|
| Verified sale `sale:S1` | Provider receivable 100.00 | Sales revenue 100.00 | Record customer sale and receivable. |
| Royalty accrual `royalty:S1:R1` | Royalty expense 30.00 | Royalty payable 30.00 | Record contractual obligation; earned is not necessarily cleared. |
| Provider settlement `settlement:T1` | Cash 100.00 | Provider receivable 100.00 | Reconcile settled proceeds before considering payable cleared. |
| Approved payout `payout:P1` | Royalty payable 30.00 | Cash 30.00 | Pay only after independent approval and verified settlement; retain payout evidence. |

A separate full-refund example assumes the first two entries exist, payment remains unsettled and royalty has not been paid: debit sales revenue 100.00 / credit provider receivable 100.00, and debit royalty payable 30.00 / credit royalty expense 30.00. Both adjustments link to the original source and refund confirmation. If proceeds already settled or royalty paid, receivable, liability or recovery treatment differs and must be approved by Finance; never delete the original entries or assume a negative balance may be collected automatically. Duplicate events with the same key and same parameters return the recorded result; reuse with different parameters is rejected. An unknown payout result is reconciled before retry, and approved payout cannot exceed the cleared payable after holds and earlier payouts.

## Cross-role checkpoint

| Role | Concern / response | Residual risk | Required approval |
|---|---|---|---|
| Finance | Balanced and replay-safe examples | Local accounting, tax and agreement treatment unapproved | Finance / qualified accountant |
| Commerce / Legal | Provider and customer remedies differ | No provider or jurisdiction verified | Commerce / Legal |

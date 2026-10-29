# DISC-04 — Business model and unit economics

Version 0.2 · 2026-10-29 · **Draft** · Author: Publishing Director · Accountable/decision owner: Executive Sponsor · Consulted: Finance, Product, Legal, Operations · Reviewer: Finance lead · Approver required: Executive Sponsor and qualified finance/legal reviewers

**Assumptions:** one curated imprint, a free portable Studio, limited text-centric catalog and one launch jurisdiction; all require validation. **Related:** DISC-01, DISC-05, DISC-06, governance decision and risk registers. **Unresolved:** prices, jurisdiction, payment provider, merchant of record, tax, royalty basis and retention; owners Finance and Publishing Director before pilot.

## Revenue and costs

Potential revenue streams are a share of eligible edition sales, optional future paid author plans and later editorial services. None is committed or priced. Free drafting may create acquisition value but incurs storage, support, conversion, security and backup cost regardless of whether a project is submitted. Curated publication adds editorial review, proofing, acquisition and rights costs per accepted title. A sale introduces payment processing, taxes, refunds and royalty liabilities. Separate operating metrics from an authoritative double-entry or balanced ledger; revenue and cash are not identical to payable royalties.

Model a cohort for a fixed period in one currency, with tax treatment explicit:

```
activated_authors = acquired_authors × activation_rate
accepted_titles = activated_authors × completion_rate × submission_rate × acceptance_rate
net_receipts = gross_sales − refunds − taxes_collected − payment_fees − channel_fees
contribution = net_receipts − royalty_expense − editorial_cost − production_cost
               − support_cost − infrastructure_cost − acquisition_cost
payable_royalty = contract-defined earned royalty − reversals − permitted recoupment
                  − prior payments, subject to clearance and contract rules
```

These are scenario relationships, not accounting policy or forecasts. Define whether taxes and fees enter the royalty base in each contract; book sales and refunds as traceable events, reconcile cleared cash and prevent payouts above cleared payable. Settle and close with qualified finance review. Do not assume a universal rate, fee or legal treatment.

## Sensitivity scenarios — inputs, not forecasts

| Scenario | Altered assumptions | Decision use |
|---|---|---|
| Lean Studio | Low submission and purchase conversion, low editorial capacity | Can storage/support be funded independently of sales? |
| Balanced curated pilot | Modest submission and limited accepted-title capacity | Does contribution per accepted title cover production and ongoing service? |
| Broader build | More channels, formats and paid features, higher fixed and integration costs | What additional throughput or margin is required to recover fixed cost? |

Finance should enter observed cohort inputs with a range, source, date and confidence; model low/base/high outcomes and sensitivity to support minutes, retention duration, refund rate, payment fees and editorial hours. An accepted title is not automatically a sale. The pilot should have an explicit loss and support capacity ceiling approved by the sponsor; numeric limits are pending actual budget.

## Go-to-market proposal

Recruit authors through writing communities, opt-in educational content and partnerships, not purchased or scraped manuscript lists. Offer useful export before any publishing decision; instrument the first chapter, not private text. Build an editorial service promise with transparent response windows once staffing is known. Reader acquisition starts with a small, rights-cleared catalog and clear descriptions, accessible previews and reliable delivery. Test search landing pages, creator partnerships and newsletter consent in one launch market before expansion. Do not claim an unvalidated conversion rate, support SLA or market size.

## Review checkpoint

| Role | Concern / response | Residual risk | Approver required |
|---|---|---|---|
| Finance | Financial dashboards can diverge from ledger; reconcile events and clearing | Pricing and payment terms absent | Finance lead |
| Legal | Rights and tax vary by market | No launch jurisdiction | Qualified counsel and tax adviser |
| Product | Free storage could be costly without conversion | No cohort data | Executive Sponsor |

References: [KDP digital pricing example](https://kdp.amazon.com/en_US/help/topic/G200634500), checked 2026-10-29, illustrates channel-specific terms, not assumed project rates; [KPI definitions](06-product-kpis-and-analytics-plan.md).

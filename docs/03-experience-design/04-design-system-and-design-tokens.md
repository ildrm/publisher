# UX-004 — Design system and design tokens

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, no human approval.
- **Authoring/accountable:** Design System Lead; **consulted:** Product, Frontend, Accessibility, Research, QA; **reviewer:** Accessibility lead; **approver/decision owner:** Product Owner. Roles are proposed.
- **Assumptions:** ASM-001–012, text-centric pilot with 2D baseline; **related requirements:** NFR-A11Y-001, NFR-I18N-001.
- **Unresolved:** OQ-002, OQ-007, OQ-010; Product and Accessibility owners resolve at prototype and pilot gates.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [screen contracts](03-screen-inventory-and-screen-specs.md), [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md), user-supplied prompt v1.0 §8.

## Token proposal

Tokens are design inputs for prototyping, not an implemented theme or evidence of accessibility conformance. Colors are specified as sRGB hex; verify every foreground/background pair after implementation and in all states.

| Token | Proposed value | Use / validation |
|---|---|---|
| `color.surface` / `color.text` | `#FFFFFF` / `#1A1A1A` | Main background/body text; contrast must be at least 4.5:1 for normal text. |
| `color.action` / `color.on-action` | `#164E9E` / `#FFFFFF` | Primary action text and fill; confirm contrast under hover and disabled states. |
| `color.danger` / `color.warning` | `#A61B1B` / `#6D4C00` | Labels and icons plus text; never use hue alone. |
| `color.border` / `color.focus` | `#666666` / `#0044CC` | Boundary/focus; indicator must be visible against adjacent surfaces. |
| `type.body` / `type.scale` | 16px base / 1.25 modular scale | User zoom/reflow supported; font selection and licensing unresolved. |
| `space.1`…`space.6` | 4, 8, 12, 16, 24, 32px | Spacing uses logical inline/block properties for RTL. |
| `radius.small` / `radius.large` | 4px / 12px | Controls / cards; no meaning encoded solely by shape. |
| `shadow.overlay` | `0 4px 16px #00000033` | Nonessential depth, never sole boundary. |
| `focus.width` / `focus.offset` | 3px / 2px | Visible persistent focus, not clipped by overflow. |
| `motion.duration` | 150ms, zero or minimal under reduced motion | Nonessential transitions only; never gate content on animation. |
| `breakpoint.compact` / `wide` | 600px / 1024px proposed | Test content reflow; not assumptions about device type. |
| `target.minimum` | 24×24 CSS px minimum, aim 44×44 | Check applicable WCAG spacing exceptions and usability. |

Components: buttons (primary/secondary/danger), labeled text fields with hints/errors, tabs, menus, status banners, dialogs with focus containment/return, tables with headers and responsive cards, upload/job progress, toast/status and pagination. Never identify errors by color only. Required values, units, allowed formats and limits are explicit next to inputs. Support browser zoom, reflow, high contrast, keyboard and screen reader. Contrast and target metrics require actual rendered measurement; do not assert a passed audit.

## Review checkpoint

| Role / concern | Response | Remaining approval |
|---|---|---|
| Accessibility: contrast/focus | Explicit tokens and test rules | Measure implemented states; Accessibility lead |
| Design: localization | Logical spacing and expansion | Test translated strings; Design lead |

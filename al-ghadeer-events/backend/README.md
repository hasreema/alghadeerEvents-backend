# Al Ghadeer Events – Backend (FastAPI + PostgreSQL)

... existing content ...

## Phase 2 additions

- Events now include financial tracking fields and status workflow (`draft|scheduled|completed|cancelled`), payment status (`unpaid|partial|paid`).
- Automatic recalculation of event `payments_total`, `expenses_total`, `labor_total`, `outstanding_amount`, and `payment_status` when payments/expenses/assignments/services change.
- New endpoints:
  - `POST /api/events/{id}/services` (name, quantity, unit_price)
  - `DELETE /api/events/{id}/services/{service_id}`
  - `POST /api/events/{id}/contacts` (name, phone?, email?, note?)
  - `DELETE /api/events/{id}/contacts/{contact_id}`
  - `POST /api/events/{id}/assignments` (employee_id?, role?, hours, hourly_rate)
  - `DELETE /api/events/{id}/assignments/{assignment_id}`

Business logic
- Payment status workflow: `unpaid` (no payments), `partial` (some payments, outstanding > 0), `paid` (outstanding <= 0). Outstanding is `quoted_total - payments_total` and never negative.
- Labor cost equals sum of assignments’ `hours * hourly_rate`.
- Quoted total defaults to sum of services if not explicitly set.
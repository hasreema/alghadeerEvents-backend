from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.payment import Payment
from app.models.expense import Expense
from app.models.event_extras import EventService, EventAssignment


def _to_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def recalc_event_financials(db: Session, event_id: int) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None

    payments_total = sum((_to_decimal(p.amount) for p in db.query(Payment).filter(Payment.event_id == event_id).all()), Decimal(0))
    expenses_total = sum((_to_decimal(x.amount) for x in db.query(Expense).filter(Expense.event_id == event_id).all()), Decimal(0))

    # services total contributes to quoted_total but could be computed directly from rows
    services_total = sum((_to_decimal(s.total_price) for s in db.query(EventService).filter(EventService.event_id == event_id).all()), Decimal(0))

    labor_total = sum((_to_decimal(a.total_cost) for a in db.query(EventAssignment).filter(EventAssignment.event_id == event_id).all()), Decimal(0))

    event.payments_total = payments_total
    event.expenses_total = expenses_total
    event.labor_total = labor_total

    if _to_decimal(event.quoted_total) == 0 and services_total > 0:
        event.quoted_total = services_total

    event.outstanding_amount = _to_decimal(event.quoted_total) - payments_total
    if event.outstanding_amount <= 0:
        event.payment_status = "paid"
        event.outstanding_amount = Decimal("0")
    elif payments_total > 0:
        event.payment_status = "partial"
    else:
        event.payment_status = "unpaid"

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
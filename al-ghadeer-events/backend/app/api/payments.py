from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.payment import Payment
from app.models.event import Event
from app.models.user import User
from app.schemas import PaymentCreate, PaymentUpdate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == payload.event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    payment = Payment(**payload.dict(), created_by=current_user.id, updated_by=current_user.id)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/", response_model=List[PaymentOut])
def list_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Payment).order_by(Payment.created_at.desc()).all()


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, payload: PaymentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    update_data = payload.dict(exclude_unset=True)
    if "event_id" in update_data:
        event = db.query(Event).filter(Event.id == update_data["event_id"]).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for k, v in update_data.items():
        setattr(payment, k, v)
    payment.updated_by = current_user.id

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return None
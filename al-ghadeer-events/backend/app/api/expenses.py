from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles, Pagination
from app.models.expense import Expense
from app.models.event import Event
from app.models.user import User
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseOut
from app.services.finance import recalc_event_financials

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.event_id is not None:
        event = db.query(Event).filter(Event.id == payload.event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    expense = Expense(**payload.dict(), created_by=current_user.id, updated_by=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)

    if expense.event_id:
        recalc_event_financials(db, expense.event_id)

    return expense


@router.get("/", response_model=List[ExpenseOut])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: Pagination = Depends(),
    event_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    query = db.query(Expense)
    if event_id is not None:
        query = query.filter(Expense.event_id == event_id)
    if category:
        query = query.filter(Expense.category == category)
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)

    return (
        query.order_by(Expense.expense_date.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, payload: ExpenseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    old_event_id = expense.event_id
    update_data = payload.dict(exclude_unset=True)
    if "event_id" in update_data and update_data["event_id"] is not None:
        event = db.query(Event).filter(Event.id == update_data["event_id"]).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for k, v in update_data.items():
        setattr(expense, k, v)
    expense.updated_by = current_user.id

    db.add(expense)
    db.commit()
    db.refresh(expense)

    if old_event_id:
        recalc_event_financials(db, old_event_id)
    if expense.event_id:
        recalc_event_financials(db, expense.event_id)

    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    event_id = expense.event_id
    db.delete(expense)
    db.commit()

    if event_id:
        recalc_event_financials(db, event_id)
    return None
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles, Pagination
from app.models.task import Task
from app.models.event import Event
from app.models.user import User
from app.schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.event_id is not None:
        event = db.query(Event).filter(Event.id == payload.event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    task = Task(**payload.dict(), created_by=current_user.id, updated_by=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: Pagination = Depends(),
    event_id: Optional[int] = Query(None, description="Filter by event_id"),
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
):
    query = db.query(Task)
    if event_id is not None:
        query = query.filter(Task.event_id == event_id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    return (
        query.order_by(Task.due_date.asc().nulls_last())
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.dict(exclude_unset=True)

    if "event_id" in update_data and update_data["event_id"] is not None:
        event = db.query(Event).filter(Event.id == update_data["event_id"]).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for key, value in update_data.items():
        setattr(task, key, value)
    task.updated_by = current_user.id

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
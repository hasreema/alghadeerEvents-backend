from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.employee import Employee
from app.models.user import User
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(["admin"]))])
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    employee = Employee(**payload.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/", response_model=List[EmployeeOut])
def list_employees(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Employee).order_by(Employee.full_name.asc()).all()


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut, dependencies=[Depends(require_roles(["admin"]))])
def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(employee, k, v)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
def delete_employee(employee_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return None
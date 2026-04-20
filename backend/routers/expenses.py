from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import schemas, crud, models
from backend.auth import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/add", response_model=schemas.Expense)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_user_expense(db=db, expense=expense, user_id=current_user.id)

@router.get("/list", response_model=List[schemas.Expense])
def list_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_expenses(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found or unauthorized")
    return {"detail": "Expense deleted successfully"}

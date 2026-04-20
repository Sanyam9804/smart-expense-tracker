from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
from backend.database import get_db
from backend import models
from backend.auth import get_current_user
from ml_model.predict import ml_engine

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning & Insights"]
)

class CategoryPredictionRequest(BaseModel):
    description: str

class InsightsResponse(BaseModel):
    predicted_next_month: float
    insights: list[str]

@router.post("/predict_category")
def predict_category(request: CategoryPredictionRequest):
    category = ml_engine.predict_category(request.description)
    return {"category": category}

@router.get("/insights", response_model=InsightsResponse)
def get_insights(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Fetch user expenses
    expenses = db.query(models.Expense).filter(models.Expense.owner_id == current_user.id).all()
    if not expenses:
        return {"predicted_next_month": 0.0, "insights": ["No expenses found. Start adding expenses to view insights."]}
    
    # Convert to df
    data = [{"date": e.date, "amount": e.amount, "category": e.category} for e in expenses]
    df = pd.DataFrame(data)
    
    insights = ml_engine.generate_insights(df)
    next_month_pred = ml_engine.predict_next_month_spending(df)
    
    return {"predicted_next_month": next_month_pred, "insights": insights}

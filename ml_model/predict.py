import joblib
import os
from datetime import datetime
from collections import defaultdict
from sklearn.linear_model import LinearRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

class ExpenseML:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model = None
            
    def predict_category(self, description: str) -> str:
        if self.model is None:
            return "Other"
        prediction = self.model.predict([description])
        return prediction[0]
        
    def predict_next_month_spending(self, historical_data: list):
        if not historical_data or len(historical_data) < 2:
            return 0.0
            
        # Group by month "YYYY-MM"
        monthly_totals = defaultdict(float)
        for row in historical_data:
            dt = datetime.fromisoformat(row['date'])
            month_key = dt.strftime("%Y-%m")
            monthly_totals[month_key] += row['amount']
            
        months_sorted = sorted(monthly_totals.keys())
        amounts = [monthly_totals[k] for k in months_sorted]
        
        if len(amounts) < 2:
            return amounts[-1] if amounts else 0.0
            
        X = [[i] for i in range(len(amounts))]
        y = amounts
        
        lr = LinearRegression()
        lr.fit(X, y)
        
        pred = lr.predict([[len(amounts)]])
        return max(0.0, float(pred[0]))
        
    def generate_insights(self, df: list) -> list:
        insights = []
        if not df:
            return ["Add more expenses to see insights."]
            
        sorted_df = sorted(df, key=lambda x: x['date'])
        
        # 1. identifying biggest category
        cat_totals = defaultdict(float)
        for expense in sorted_df:
            cat_totals[expense['category']] += expense['amount']
            
        if cat_totals:
            top_cat = max(cat_totals.items(), key=lambda x: x[1])
            insights.append(f"Most of your spending is on **{top_cat[0]}** (₹{top_cat[1]:.2f}).")
        
        # 2. total spent
        total = sum(x['amount'] for x in sorted_df)
        insights.append(f"Total spent so far gives you a baseline of ₹{total:.2f}.")
        
        # 3. Simple trend if taking diff over weeks
        weekly = defaultdict(float)
        for expense in sorted_df:
            dt = datetime.fromisoformat(expense['date'])
            # year and ISO week
            week_key = f"{dt.isocalendar()[0]}-{dt.isocalendar()[1]:02d}"
            weekly[week_key] += expense['amount']
            
        weeks_sorted = sorted(weekly.keys())
        if len(weeks_sorted) >= 2:
            last_week = weekly[weeks_sorted[-2]]
            this_week = weekly[weeks_sorted[-1]]
            if last_week > 0:
                pct_change = ((this_week - last_week) / last_week) * 100
                if pct_change > 0:
                    insights.append(f"Your spending increased by {pct_change:.1f}% this week compared to last.")
                else:
                    insights.append(f"Great! Your spending decreased by {abs(pct_change):.1f}% this week compared to last.")
                    
        return insights

ml_engine = ExpenseML()

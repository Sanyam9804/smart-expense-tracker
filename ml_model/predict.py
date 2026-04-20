import joblib
import os
import pandas as pd
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
            # If model doesn't exist to prevent crash
            self.model = None
            
    def predict_category(self, description: str) -> str:
        if self.model is None:
            # Fallback
            return "Other"
        prediction = self.model.predict([description])
        return prediction[0]
        
    def predict_next_month_spending(self, historical_data: pd.DataFrame):
        # Expects dataframe with 'date' and 'amount'
        if historical_data.empty or len(historical_data) < 2:
            return 0.0
            
        # Group by month
        historical_data['month'] = pd.to_datetime(historical_data['date']).dt.to_period('M')
        monthly_totals = historical_data.groupby('month')['amount'].sum().reset_index()
        
        if len(monthly_totals) < 2:
            return monthly_totals['amount'].iloc[-1] if not monthly_totals.empty else 0.0
            
        # Very simple linear regression for forecasting
        monthly_totals['time_idx'] = range(len(monthly_totals))
        X = monthly_totals[['time_idx']]
        y = monthly_totals['amount']
        
        lr = LinearRegression()
        lr.fit(X, y)
        
        next_month_idx = len(monthly_totals)
        pred = lr.predict([[next_month_idx]])
        return max(0, pred[0])
        
    def generate_insights(self, df: pd.DataFrame) -> list:
        insights = []
        if df.empty:
            return ["Add more expenses to see insights."]
            
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        
        # 1. identifying biggest category
        category_sums = df.groupby('category')['amount'].sum()
        top_cat = category_sums.idxmax()
        insights.append(f"Most of your spending is on **{top_cat}** (₹{category_sums[top_cat]:.2f}).")
        
        # 2. total spent
        total = df['amount'].sum()
        insights.append(f"Total spent so far gives you a baseline of ₹{total:.2f}.")
        
        # 3. Simple trend if taking diff over weeks
        df['week'] = df['date'].dt.isocalendar().week
        weekly = df.groupby('week')['amount'].sum()
        if len(weekly) >= 2:
            last_week = weekly.iloc[-2]
            this_week = weekly.iloc[-1]
            if last_week > 0:
                pct_change = ((this_week - last_week) / last_week) * 100
                if pct_change > 0:
                    insights.append(f"Your spending increased by {pct_change:.1f}% this week compared to last.")
                else:
                    insights.append(f"Great! Your spending decreased by {abs(pct_change):.1f}% this week compared to last.")
                    
        return insights

ml_engine = ExpenseML()

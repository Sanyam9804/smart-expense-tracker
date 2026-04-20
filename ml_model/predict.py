import os
from datetime import datetime
from collections import defaultdict

class ExpenseML:
    def __init__(self):
        pass
        
    def predict_category(self, description: str) -> str:
        desc = description.lower()
        if any(word in desc for word in ['coffee', 'starbucks', 'dinner', 'lunch', 'food', 'market']):
            return 'Food & Dining'
        if any(word in desc for word in ['grocery', 'whole foods', 'walmart', 'supermarket']):
            return 'Groceries'
        if any(word in desc for word in ['rent', 'mortgage', 'apartment']):
            return 'Housing'
        if any(word in desc for word in ['uber', 'gas', 'transit', 'car', 'ride']):
            return 'Transportation'
        if any(word in desc for word in ['netflix', 'spotify', 'movie', 'game', 'gym']):
            return 'Entertainment'
        if any(word in desc for word in ['doctor', 'pharmacy', 'hospital', 'medicine']):
            return 'Health'
        if any(word in desc for word in ['electric', 'water', 'internet', 'bill']):
            return 'Utilities'
        if any(word in desc for word in ['amazon', 'clothes', 'shoe', 'shopping']):
            return 'Shopping'
        return "Other"
        
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
            
        if len(amounts) < 2:
            return amounts[-1] if amounts else 0.0
            
        # Simple moving average heuristic instead of sklearn Linear Regression
        avg_increase = (amounts[-1] - amounts[0]) / len(amounts)
        return max(0.0, amounts[-1] + avg_increase)
        
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

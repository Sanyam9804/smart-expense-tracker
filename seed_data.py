import datetime
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend import models, crud, schemas
from backend.auth import get_password_hash

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    
    # 1. Create User
    username = "test1"
    password = "1234"
    
    user = crud.get_user_by_username(db, username=username)
    if not user:
        hashed_pw = get_password_hash(password)
        user = models.User(username=username, hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user: {username}")
    else:
        print(f"User {username} already exists. Using existing ID: {user.id}")

    # 2. Delete existing expenses for this user to make it clean
    db.query(models.Expense).filter(models.Expense.owner_id == user.id).delete()
    db.commit()

    # 3. Add Dummy Expenses
    today = datetime.date.today()
    expenses_data = [
        {"desc": "Starbucks Coffee", "amt": 5.50, "cat": "Food & Dining", "days_offset": 0},
        {"desc": "Whole Foods Groceries", "amt": 120.00, "cat": "Groceries", "days_offset": -1},
        {"desc": "Netflix Subscription", "amt": 15.99, "cat": "Entertainment", "days_offset": -2},
        {"desc": "Uber Ride", "amt": 24.50, "cat": "Transportation", "days_offset": -2},
        {"desc": "Apartment Rent", "amt": 1500.00, "cat": "Housing", "days_offset": -5},
        {"desc": "Gym Membership", "amt": 45.00, "cat": "Health", "days_offset": -7},
        {"desc": "Electricity Bill", "amt": 85.20, "cat": "Utilities", "days_offset": -10},
        {"desc": "Amazon Shopping", "amt": 64.99, "cat": "Shopping", "days_offset": -12},
        {"desc": "Salad for Lunch", "amt": 12.00, "cat": "Food & Dining", "days_offset": -14},
        {"desc": "Gas Station", "amt": 40.00, "cat": "Transportation", "days_offset": -15},
        {"desc": "Dinner with friends", "amt": 85.00, "cat": "Food & Dining", "days_offset": -20},
        {"desc": "Internet Bill", "amt": 60.00, "cat": "Utilities", "days_offset": -25},
    ]

    for item in expenses_data:
        exp_date = today + datetime.timedelta(days=item["days_offset"])
        db_expense = models.Expense(
            amount=item["amt"],
            category=item["cat"],
            date=exp_date,
            description=item["desc"],
            payment_mode="Card" if item["amt"] > 50 else "Cash",
            owner_id=user.id
        )
        db.add(db_expense)
    
    db.commit()
    print("Successfully added dummy expenses!")
    db.close()

if __name__ == "__main__":
    seed_db()

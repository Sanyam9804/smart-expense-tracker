# 🧠 Smart Expense Tracker SaaS

A production-grade, AI-powered Smart Expense Tracker built with Python, FastAPI, and Vanilla JS.

This application allows users to securely track expenses, automatically categorize transactions using a built-in Natural Language Processing (NLP) Machine Learning model, predict future spending via regression, and visualize trend data through a stunning glassmorphism Single Page Application (SPA).

---

## 🚀 Features

- **JWT Authentication**: Secure, multi-tenant sign-in capabilities.
- **AI Auto-Categorization**: Enter "Starbucks" or "Taxi", and the background Scikit-Learn Logistic Regression model accurately tags your expense categories! 
- **Predictive Analytics Engine**: Employs mathematical trend analysis to forecast your next month's spending directly on the dashboard.
- **Premium Glassmorphism UI**: Beautifully designed from scratch using Vanilla CSS to eliminate build steps while ensuring a responsive, high-end "real-world" aesthetic.
- **Actionable Insights**: Generate real-time budget warnings and weekly trend comparisons based on your exact historical ledger.
- **Docker & Vercel Ready**: Comes with standard `docker-compose` integrations and a `vercel.json` routing layer for immediate Serverless Python deployment.

---

## 🧱 Architecture

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (No-Build SPA)
- **Backend APIs**: FastAPI (Python)
- **Database**: SQLite integrated with SQLAlchemy
- **Machine Learning**: Scikit-learn (`TfidfVectorizer` + `LogisticRegression`)
- **Charting**: Chart.js 

---

## 🛠️ Local Setup Instructions

### 1. Standard Python Setup
```bash
# Initialize and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the ML model and set up mock data
python seed_data.py
python ml_model/train_model.py

# Run the localized FastAPI and UI Server
uvicorn backend.main:app --host 127.0.0.1 --port 8080
```
Then visit `http://localhost:8080` in your browser.

### 2. Docker Setup (Optional)
```bash
docker-compose up --build
```
Your backend will route natively, allowing cross-container communication.

---

## ☁️ Vercel Deployment

This project natively supports Vercel's Serverless Python Architecture! 
1. Push this repository to GitHub.
2. Link the repository to your Vercel Dashboard.
3. Vercel automatically reads `vercel.json` and spins up the backend serverless endpoints to proxy traffic properly, serving your HTML/CSS blazingly fast.

*(Note: Vercel serverless environments are ephemeral. You must modify `backend/database.py` to point to a permanent Cloud Database like Neon Postgres or Supabase before putting it into actual production).*

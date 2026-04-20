from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routers import auth, expenses, ml_insights
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(ml_insights.router)

# Serve static files for frontend conditionally
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public")

@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "Vercel API is running successfully!"}

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path), name="static")

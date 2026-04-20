from fastapi import FastAPI

app = FastAPI()

@app.get("/auth/")
@app.get("/docs")
@app.get("/api/test")
def test_route():
    return {"message": "Success! The bug is inside backend/main.py imports."}

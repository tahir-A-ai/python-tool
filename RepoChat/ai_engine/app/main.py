from fastapi import FastAPI
from app.api import routes

# 1. Initialize the App
app = FastAPI(title="RepoRAG AI Engine")

# 2. Connect the Routes (The Endpoints)
app.include_router(routes.router)

# 3. Basic Health Check
@app.get("/")
def health_check():
    return {"status": "running", "service": "AI Engine"}
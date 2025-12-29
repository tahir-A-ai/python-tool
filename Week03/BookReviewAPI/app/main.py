from fastapi import FastAPI
from app.routers import auth, reviews

# Initializing the App
app = FastAPI(
    title="Book Review API",
    version="1.0.0",
    description="A professional API with Auth, RBAC, and Database relationships."
)

# 2. Include the Routers
# This tells FastAPI: "Go look in auth.py for more URL paths"
app.include_router(auth.router)
app.include_router(reviews.router)

# 3. Root Endpoint (Health Check)
@app.get("/")
def read_root():
    return {"message": "Book Review API is running!"}
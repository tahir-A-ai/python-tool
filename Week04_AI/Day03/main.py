from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Import the logic we just wrote
from services import generate_keywords, generate_bullet_points

app = FastAPI(title="AI Utilities API", version="1.0")

# Input Model (Data Validation)
class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "AI Utilities System Online!"}

@app.post("/extract-keywords")
async def get_keywords(request: TextRequest):
    """Returns a JSON list of key topics."""
    try:
        keywords = generate_keywords(request.text)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize-bullets")
async def get_notes(request: TextRequest):
    """Converts text to emoji bullet points."""
    try:
        notes = generate_bullet_points(request.text)
        return {"notes": notes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
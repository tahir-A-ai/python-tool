from pydantic import BaseModel

class IngestPayload(BaseModel):
    # incoming data from django
    repo_id: int
    file_path: str

class SearchPayload(BaseModel):
    query: str
    limit: int = 3  # Retrieve top 3 results by default


    # Example for documentation (Swagger UI will show this)
class Config:
    json_schema_extra = {
        "example": {
            "query": "How do I log in?",
            "limit": 3
            }
        }
    

class ChatPayload(BaseModel):
    repo_id: int
    query: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_id": 15,
                "query": "Explain how the division function handles errors."
            }
        }
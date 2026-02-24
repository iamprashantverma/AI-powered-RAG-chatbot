from pydantic import BaseModel, Field,ConfigDict

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=500)

class ChatResponse(BaseModel):
    id: int
    role: str
    content: str
    model_config = ConfigDict(from_attributes=True)
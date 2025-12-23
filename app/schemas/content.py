from pydantic import BaseModel, Field


class ContentCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="Add details about the content")
    category: str = Field(..., min_length=1, max_length=100, description="Category of the content")
    tags: list[str] = Field(default=[], description="List of tags associated with the content")
    
class ContentCreateResponse(BaseModel):
    success: bool



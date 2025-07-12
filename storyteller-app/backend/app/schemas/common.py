from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional

DataType = TypeVar('DataType')

class PaginatedResponse(BaseModel, Generic[DataType]):
    count: int = Field(..., description="Total number of items")
    page: Optional[int] = Field(None, description="Current page number")
    page_size: Optional[int] = Field(None, description="Number of items per page")
    total_pages: Optional[int] = Field(None, description="Total number of pages")
    items: List[DataType] = Field(..., description="List of items for the current page")

class MessageResponse(BaseModel):
    message: str

# Example of a simple ID request, if needed for some POST/PATCH operations
class IdRequest(BaseModel):
    id: int

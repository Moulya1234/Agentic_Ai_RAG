from typing import List,Dict,Any,Optional
from pydantic import BaseModel,Field
from datetime import datetime

class ResearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The research question")
    num_results: Optional[int] = Field(default=5, ge=1, le=10, description="Number of search results")
    stream: Optional[bool] = Field(default=True, description="Whether to stream the response")

    class Config:
        schema_extra = {
            "example": {
                "query": "What are the latest developments in quantum computing?",
                "num_results": 5,
                "stream": True
            }
        }
class Source(BaseModel):
    title:str
    url:str
    highlights:Optional[List[str]]=[]
    published_date:Optional[str]=None
    author:Optional[str]=None

class ResearchResponse(BaseModel):
    query:str
    answer:str
    sources:List[Source]
    research_time_seconds:float
    timestamp:datetime=Field(default_factory=datetime.now(datetime.timezone.utc))
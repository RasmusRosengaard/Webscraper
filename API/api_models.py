from typing import List, Optional, Dict
from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    urls: List[str]
    elements: Optional[List[str]] = None  # None => scrape alt


class ScrapeResult(BaseModel):
    url: str
    status: int
    content: Dict[int, str]

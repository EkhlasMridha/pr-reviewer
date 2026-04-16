from pydantic import BaseModel
from typing import List

class Issue(BaseModel):
    file: str
    line: int
    severity: str
    comment: str
    suggestion: str

class ReviewResult(BaseModel):
    summary: str
    issues: List[Issue]
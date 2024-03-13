from typing import List
from pydantic import BaseModel


class Table(BaseModel):
    line_start: int
    line_end: int
    included_text: List[str]


class Tables(BaseModel):
    tables: List[Table]

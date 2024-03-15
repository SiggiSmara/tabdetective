from typing import List, Dict
from pydantic import BaseModel


class Table(BaseModel):
    line_start: int
    line_end: int
    raw_text: List[str]
    headers: List[str]
    rows: List[Dict]


class FoundTable(BaseModel):
    my_table: Table
    line_end: int

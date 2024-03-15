from typing import List, Dict, Any
from pydantic import BaseModel


class Row(BaseModel):
    cells: List[Any]


class ContiguousLine(BaseModel):
    line_no: int
    col_count: int
    row: Row


class ColPos(BaseModel):
    start: int
    end: int


class DetectorModel(BaseModel):
    name: str
    min_numrows: int
    first_row_is_header: bool


class CharDelimiterModel(DetectorModel):
    delimiter: str
    min_cols: int


class MarkdownDelimiterModel(CharDelimiterModel):
    delimiter: str = "|"
    first_row_is_header: bool = False


class SpaceDelimiterModel(CharDelimiterModel):
    delimiter: str = " "
    col_positions: List[ColPos]

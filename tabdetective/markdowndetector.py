from tabdetective.chardetector import CharDetector
from tabdetective.objects.tables import Table
from tabdetective.objects.detectormodel import (
    MarkdownDelimiterModel,
    ContiguousLine,
    Row,
)
from typing import List, Union
from pathlib import Path


class MarkdownDetector(CharDetector):
    """Detect potential tables that are separated by a specific delimiter character."""

    def __init__(self, model: MarkdownDelimiterModel):
        # super().__init__(model)
        self._model: MarkdownDelimiterModel = model
        self._tables: List[Table] = None
        self._text: List[str] = None

    def detect(self, filepath: Path, endoding: str = "utf-8") -> Union[int, bool]:
        """Looks for markdown style tables in the file"""
        super().detect(filepath, endoding)
        ## Add markdown specific detection here
        # such as the header being separated from the body by a line of dashes
        # and the table being surrounded by lines of dashes (top and bottom)
        # and the first and last delimiters of a row act as surrounding lines as well

        if self._tables is not None:
            return len(self._tables)

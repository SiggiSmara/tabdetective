from tabdetective.detector import Detector
from tabdetective.objects.tables import Table, FoundTable
from tabdetective.objects.detectormodel import CharDelimiterModel, ContiguousLine, Row
from typing import List, Union
from pathlib import Path


class CharDetector(Detector):
    """Detect potential tables that are separated by a specific delimiter character."""

    def __init__(self, model: CharDelimiterModel):
        # super().__init__(model)
        self._model: CharDelimiterModel = model
        self._tables: List[Table] = None
        self._text: List[str] = None

    def detect(self, filepath: Path, endoding: str = "utf-8") -> Union[int, bool]:
        """Looks for lines that have x delimiter characters (x defined in the model)
        and determines if they meet consistency criteria also
        defined in the model.
        """
        self._read(filepath, endoding)
        found_lines: List[ContiguousLine] = []
        for i, line in enumerate(self._text):
            if line.count(self._model.delimiter) >= self._model.min_cols:
                my_row: Row = Row(
                    cells=[x.strip() for x in line.split(self._model.delimiter)]
                )
                found_lines.append(
                    ContiguousLine(line_no=i, col_count=len(my_row.cells), row=my_row)
                )

        self._tables: List[Table] = None
        while len(found_lines) > 0:
            found_table: FoundTable = self._find_table(found_lines)
            if found_table is not None:
                if self._tables is not None:
                    self._tables.append(found_table.my_table)
                else:
                    self._tables = [
                        found_table.my_table,
                    ]
                del found_lines[0 : found_table.line_end + 1]
            else:
                del found_lines[0]
        if self._tables is not None:
            return len(self._tables)

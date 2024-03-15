from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List
from tabdetective.objects.tables import Table, FoundTable
from tabdetective.objects.detectormodel import DetectorModel, ContiguousLine


class Detector(ABCMeta):
    def __init__(self, model: DetectorModel):
        """Parent detector class. It requires a model definition (dict) to be passed
        when instantiated. This model is then to be used in the child classes to
        detect tables in files.

        Args:
            model (DetectorModel): The model definition to be used by the child classes.
        """
        self._model: DetectorModel = model
        self._tables: List[Table] = None
        self._text: List[str] = None

    @abstractmethod
    def detect(self, filepath: Path, endoding: str = "utf-8"):
        """The parent method to be implemented by the child classes
        for different detectors.

        Args:
            filepath (Path): the path to the file with a suspected table.
            endoding (str, optional): the valid python encoding str to be used to read the file. Defaults to "utf-8".
        """
        pass

    def _read(self, filepath: Path, endoding: str, striplines: bool = True):
        """Reads a file with a certain encoding and stores the text in the _text attribute
        as a line splitted list. It can also strip all non-printing characters from the lines
        before storing them in self._text.

        Args:
            filepath (Path): the path to the file.
            endoding (str): the valid python encoding str to be used to read the file.
            striplines (bool, optional): If True, all non-printing characters are stripped from the lines. Defaults to True.
        """
        with open(filepath, "r", encoding=endoding) as f:
            if striplines:
                self._text = [x.strip() for x in f.read().splitlines()]
            else:
                self._text = f.read().splitlines()

    def _find_table(
        self, found_lines: List[ContiguousLine], line_start: int = 0
    ) -> FoundTable:
        """Finds a table in the found_lines list. It looks for contiguous lines
        that have the same number of detected columns. If the number of contiguous
        lines is equal or greater than the min_numrows defined in the model, it
        returns a Tables object with the found table and the line number where the
        table ends.

        Args:
            found_lines (List[int]): The list of lines that have been detected as potential tables.
            line_start (int, optional): The starting line to begin the detection. Defaults to 0.

        Returns:
            FoundTable: The FoundTable object with the table and the line number where the table ends.
        """
        found_table: FoundTable = None
        contiguous_lines: List[ContiguousLine] = []
        for i in range(start=line_start, stop=len(found_lines) - 1):
            if (
                found_lines[i + 1].line_no - found_lines[i].line_no == 1
                and found_lines[i + 1].col_count == found_lines[i].col_count
            ):
                contiguous_lines.append(found_lines[i])
            if len(contiguous_lines) >= self._model.min_numrows:
                if self._model.first_row_is_header:
                    header = [x for x in contiguous_lines[0].row.cells]
                else:
                    header = [
                        "col_" + str(x).fill(len(str(found_lines[0].col_count)))
                        for x in range(found_lines[0].col_count)
                    ]
                found_table = Table(
                    line_start=contiguous_lines[0].line_no,
                    line_end=contiguous_lines[-1].line_no,
                    raw_text=self._text[
                        contiguous_lines[0].line_no : contiguous_lines[-1].line_no + 1
                    ],
                    headers=header,
                    rows=[dict(zip(header, x.row.cells)) for x in contiguous_lines],
                )
        return FoundTable(found_table=found_table, line_end=contiguous_lines[-1])

    @property
    def tables(self):
        """This is the tables property. It is a read only property as the table definition
        is the result of the table detection method and can only be changed via calling the
        detect method.
        """
        return self._tables

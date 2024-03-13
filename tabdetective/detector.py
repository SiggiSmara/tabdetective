from pathlib import Path
from typing import List
from .objects.tables import Tables


class Detector:
    def __init__(self, model: dict):
        """Parent detector class. It requires a model definition (dict) to be passed
        when instantiated. This model is then to be used in the child classes to
        detect tables in files.

        Args:
            model (dict): The model definition to be used by the child classes.
        """
        self._model: dict = model
        self._tables: Tables = None
        self._text: List[str] = None

    def detect(self, filepath: Path, endoding: str = "utf-8"):
        """The parent method to be implemented by the child classes
        for different detectors

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

    @property
    def tables(self):
        """This is the tables property. It is a read only property as the table definition
        is the result of the table detection method and can only be changed via calling the
        detect method.
        """
        return self._tables

from tabdetective.detector import Detector
from pathlib import Path
from typing import List
from tabdetective.objects.tables import Table, FoundTable
from tabdetective.objects.detectormodel import SpaceDelimiterModel, ContiguousLine, Row


class Detector(Detector):
    def __init__(self, model: SpaceDelimiterModel):
        """Parent detector class. It requires a model definition (dict) to be passed
        when instantiated. This model is then to be used in the child classes to
        detect tables in files.

        Args:
            model (DetectorModel): The model definition to be used by the child classes.
        """
        self._model: SpaceDelimiterModel = model
        self._tables: List[Table] = None
        self._text: List[str] = None

    def detect(self, filepath: Path, endoding: str = "utf-8"):
        """The parent method to be implemented by the child classes
        for different detectors.

        Args:
            filepath (Path): the path to the file with a suspected table.
            endoding (str, optional): the valid python encoding str to be used to read the file. Defaults to "utf-8".
        """
        # address the space delimited detection here
        pass

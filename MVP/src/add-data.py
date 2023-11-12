from dataclasses import dataclass
from typing import Union, List, Optional


class Image:
    pass


class Video:
    pass


class Text:
    pass


class Audio:
    pass


@dataclass
class Data:
    data: Union[Image, Video, Text, Audio]
    name: str


class PointsOfInterest:
    pass


class Token:
    pass


class AddDataModule:

    def is_applicable(self, data: Data) -> bool:
        pass

    def split_data_into_points_of_interest(self, data: Data) -> List[PointsOfInterest]:
        pass

    def tokenize_point_of_interest(self, poi: PointsOfInterest) -> List[Token]:
        pass


class DataAdder:

    def __init__(self, modules: List[AddDataModule]):
        self.modules = modules

    def add_data(self, data: Data):
        module = self._get_module(data)
        if module is None:
            raise NotImplementedError
        pois = module.split_data_into_points_of_interest(data)
        tokens = ...

    def _get_module(self, data: Data) -> Optional[AddDataModule]:
        for module in self.modules:
            if module.is_applicable(data):
                return module
        return None


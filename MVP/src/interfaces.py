from abc import ABC
from typing import TypeVar, Generic

from result import Result

Data = TypeVar("Data")
Request = TypeVar("Request")
Response = TypeVar("Response")


class DataAdderInterface(ABC, Generic[Data, Response]):

    def add_data(self, data: Data) -> Result[Response]:
        pass


class DataGetterInterface(ABC, Generic[Response]):

    def get_data(self, query: str) -> Result[Response]:
        pass


class DataRemoverInterface(ABC, Generic[Response]):

    def remove_data(self, data_id: str) -> Result[Response]:
        pass


class TokenAdderInterface(ABC, Generic[Request, Response]):

    def add_token(self, request: Request) -> Result[Response]:
        pass


class TokenRemoverInterface(ABC, Generic[Response]):

    def remove_token(self, token: str) -> Result[Response]:
        pass


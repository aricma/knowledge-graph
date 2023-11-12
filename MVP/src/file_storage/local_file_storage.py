import dataclasses
from pathlib import Path
from typing import Dict
from uuid import uuid4

AbsolutePath = str
FileID = str
URI = str


@dataclasses.dataclass
class AddFileResponse:
    id: FileID
    uri: URI


@dataclasses.dataclass
class GetFileResponse:
    id: FileID
    uri: URI
    content: bytes


class LocalFileStorage:
    _id_to_uri_map: Dict[FileID, URI]
    _storage_directory: Path

    def __init__(self, storage_directory: AbsolutePath):
        self._id_to_uri_map = dict()
        self._storage_directory: Path = Path(storage_directory)
        self._storage_directory.mkdir(
            parents=True,
            exist_ok=True,
            mode=0o777,
        )

    def add(self, file: bytes, name: str) -> AddFileResponse:
        uri = self._make_uri(name)
        if self._has_file_uri(uri):
            raise ValueError(f"File with given name: {name} already exists!")
        with open(uri, "wb") as writer:
            writer.write(file)
        if not self._has_file_uri(uri):
            raise FileNotFoundError(f"Failed to store the file with name: {name}!")
        file_id = self._generate_new_id()
        self._id_to_uri_map[file_id] = uri
        return AddFileResponse(
            id=file_id,
            uri=uri,
        )

    def get(self, file_id: FileID) -> GetFileResponse:
        uri = self._get_file_uri_from(file_id)
        with open(uri, "rb") as reader:
            content = reader.read()
        return GetFileResponse(
            id=file_id,
            uri=uri,
            content=content
        )

    def remove(self, file_id: FileID) -> None:
        uri = self._get_file_uri_from(file_id)
        Path(uri).unlink()
        # check if file is gone and mapping is reduced

    def _get_file_uri_from(self, file_id: FileID) -> URI:
        if self._has_file_id(file_id) is None:
            raise FileNotFoundError(f"Found no URI for given file id: {file_id}!")
        uri = self._id_to_uri_map.get(file_id)
        if not self._has_file_uri(uri):
            raise FileNotFoundError(f"Failed to get file with id: {file_id} and uri: {uri}!")
        return uri

    def _has_file_id(self, file_id: FileID) -> bool:
        return self._id_to_uri_map.get(file_id) is None

    def _make_uri(self, name: str) -> URI:
        return str(self._storage_directory / name)

    def _generate_new_id(self) -> FileID:
        new_id = uuid4()
        while new_id in self._id_to_uri_map.keys():
            new_id = uuid4()
        return str(new_id)

    @staticmethod
    def _has_file_uri(uri: URI) -> bool:
        return Path(uri).exists()


if __name__ == '__main__':
    ls = LocalFileStorage("/tmp")
    add_file_res = ls.add(
        name="foo",
        file=bytes("hello world!".encode("utf8"))
    )

    print(add_file_res)

    get_file_res = ls.get(
        file_id=add_file_res.id
    )

    print(get_file_res)

    ls.remove(
        file_id=add_file_res.id
    )

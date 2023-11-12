import dataclasses
import json
import sqlite3
from typing import Any, Dict, List, Optional
from uuid import uuid4

ChunkID = str


@dataclasses.dataclass
class Chunk:
    id: ChunkID
    original_file_id: str
    content: str
    meta_data: Dict[str, Any]


@dataclasses.dataclass
class AddChunkRequest:
    original_file_id: str
    content: str
    meta_data: Dict[str, Any]


@dataclasses.dataclass
class AddChunkResponse:
    chunk_id: ChunkID


class SQLiteChunkStorage:
    database: sqlite3.Connection

    def __init__(self, database: sqlite3.Connection):
        self.database = database

    def add_chunks(self, chunks: List[AddChunkRequest]) -> List[Optional[AddChunkResponse]]:
        data = [
            (
                self._generate_id(),
                chunk.content,
                json.dumps(chunk.meta_data),
                chunk.original_file_id,
            ) for chunk in chunks
        ]
        self.database.executemany("INSERT INTO chunks VALUES(?, ?, ?, ?)", data)
        self.database.commit()

        return [
            AddChunkResponse(
                chunk_id=record[0]
            ) for record in data
        ]

    def get_chunks(self, chunk_ids: List[ChunkID]) -> List[Chunk]:
        placeholders = ', '.join('?' * len(chunk_ids))
        query = f"SELECT * FROM chunks WHERE id IN ({placeholders})"
        response = self.database.execute(query, chunk_ids).fetchall()
        self.database.commit()
        return [
            Chunk(
                id=each[0],
                content=each[1],
                meta_data=json.loads(each[2]),
                original_file_id=each[3],
            ) for each in response
        ]

    def _generate_id(self) -> str:
        all_ids = self.database.execute("SELECT id from chunks").fetchall()
        new_id = str(uuid4())
        while new_id in all_ids:
            new_id = str(uuid4())
        return new_id


if __name__ == '__main__':
    db = sqlite3.connect(":memory:")

    # create tables
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE chunks (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            meta_data TEXT NOT NULL,
            original_file_id TEXT
        );
    """)
    db.commit()

    cs = SQLiteChunkStorage(database=db)
    res_1 = cs.add_chunks([AddChunkRequest(
        original_file_id="foo",
        content="bar",
        meta_data={"baz": "foobar"}
    )])

    print(res_1)

    res_2 = cs.add_chunks([AddChunkRequest(
        original_file_id="moo",
        content="chu",
        meta_data={"in": "on"}
    )])

    print(res_2)

    all_responses = res_1 + res_2
    all_response_ids = [each.chunk_id for each in all_responses]
    res_3 = cs.get_chunks(all_response_ids)
    db.commit()

    print(res_3)

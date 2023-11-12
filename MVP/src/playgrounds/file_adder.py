import dataclasses
import sqlite3
from pathlib import Path
from typing import List, Dict

from chunk_storage.sqlite_chunk_storage import SQLiteChunkStorage, Chunk, AddChunkRequest
from file_loader.py_pdf_file_loader import PyPDFFileLoader
from file_splitter.text_file_splitter import TextFileSplitter
from file_storage.local_file_storage import LocalFileStorage
from playgrounds.models import QueryResult, OriginalFileID, MatchingChunk
from vector_db.in_memory_vector_db import InMemoryChromaVectorDB, Chunk as VectorDBChunk


@dataclasses.dataclass
class AddFileResponse:
    storage_id: str


class FileAdder:
    _chroma_db_collection = "default"

    def __init__(self, storage_directory: str, file_loader_temp_directory: str):
        self._file_storage = LocalFileStorage(storage_directory=storage_directory)
        self._vector_db = InMemoryChromaVectorDB()
        self._text_file_splitter = TextFileSplitter(
            chunk_size=250,
            chunk_overlap=50,
        )
        self._pdf_file_loader = PyPDFFileLoader(temp_directory=file_loader_temp_directory)
        database = sqlite3.connect(":memory:")
        # create tables
        cur = database.cursor()
        cur.execute("""
                CREATE TABLE chunks (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    meta_data TEXT NOT NULL,
                    original_file_id TEXT
                );
            """)
        database.commit()
        self._chunk_storage = SQLiteChunkStorage(database)

    def add_file(self, file: bytes, name: str) -> AddFileResponse:
        if name.endswith(".pdf") or name.endswith(".PDF"):
            return self.add_pdf_file(file=file, name=name)
        if name.endswith(".txt"):
            return self.add_plain_text_file(file=file, name=name)
        else:
            raise ValueError("Your given file has no extension.")

    def add_pdf_file(self, file: bytes, name: str) -> AddFileResponse:
        add_file_storage_response = self._file_storage.add(file=file, name=name)
        pdf_file_as_plain_text_files = self._pdf_file_loader.load(file=file)
        chunks = list()
        for plain_text_file in pdf_file_as_plain_text_files:
            chunks = chunks + self._chunkify_the_file(
                file_content=plain_text_file.content,
                original_file_id=add_file_storage_response.id,
            )
        self._vectorise_chunks(chunks)
        return AddFileResponse(
            storage_id=add_file_storage_response.id,
        )

    def add_plain_text_file(self, file: bytes, name: str) -> AddFileResponse:
        add_file_storage_response = self._file_storage.add(file=file, name=name)
        chunks = self._chunkify_the_file(
            file_content=file.decode("utf-8"),
            original_file_id=add_file_storage_response.id,
        )
        self._vectorise_chunks(chunks)
        return AddFileResponse(
            storage_id=add_file_storage_response.id,
        )

    def query(self, query: str) -> List[QueryResult]:
        query_responses_ordered_by_original_file_id: Dict[OriginalFileID, QueryResult] = dict()
        vector_db_query_responses = self._vector_db.query(
            collection_name=self._chroma_db_collection,
            query=query
        )
        all_related_chunks = self._chunk_storage.get_chunks([
            each.match.chunk_id for each in vector_db_query_responses
        ])
        all_related_original_files = [
            self._file_storage.get(each.original_file_id)
            for each in all_related_chunks
        ]
        all_data = zip(vector_db_query_responses, all_related_chunks, all_related_original_files)
        for match, chunk, file in all_data:
            new_matching_chunk = MatchingChunk(
                content=chunk.content,
                confidence=match.distance,
            )
            if file.id not in query_responses_ordered_by_original_file_id.keys():
                query_response = QueryResult(
                    query=match.query,
                    matching_chunks=[new_matching_chunk],
                    original_file=file.uri,
                )
            else:
                query_response = query_responses_ordered_by_original_file_id[file.id]
                query_response.matching_chunks.append(new_matching_chunk)
            query_responses_ordered_by_original_file_id[file.id] = query_response

        return list(query_responses_ordered_by_original_file_id.values())

    def remove_file(self, file_id: str) -> None:
        self._file_storage.remove(file_id)

    def _chunkify_the_file(self, file_content: str, original_file_id: str) -> List[Chunk]:
        chunks = self._text_file_splitter.recursively_split_by_characters(file_content)
        chunks_added_to_storage = self._chunk_storage.add_chunks([
            AddChunkRequest(
                content=chunk.content,
                meta_data=chunk.meta_data,
                original_file_id=original_file_id,
            ) for chunk in chunks
        ])
        return self._chunk_storage.get_chunks([
            each.chunk_id for each in chunks_added_to_storage
        ])

    def _vectorise_chunks(self, chunks: List[Chunk]) -> None:
        self._vector_db.add_chunks_to_collection(
            collection_name=self._chroma_db_collection,
            chunks=[
                VectorDBChunk(
                    id=chunk.id,
                    content=chunk.content,
                    meta_data=chunk.meta_data,
                ) for chunk in chunks
            ]
        )

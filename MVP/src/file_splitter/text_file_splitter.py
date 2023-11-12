import dataclasses
from typing import List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter


@dataclasses.dataclass
class Chunk:
    content: str
    meta_data: Dict[str, Any]


class TextFileSplitter:

    _chunk_size: int = 25
    _chunk_overlap: int = 0

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def recursively_split_by_characters(self, file_content: str) -> List[Chunk]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["/n/n", "/n", ". ", ", ", " ", ""],
            # add_start_index=True,
            strip_whitespace=True,
            keep_separator=True,
        )
        documents = text_splitter.create_documents([file_content])
        return [
            Chunk(
                content=document.page_content,
                meta_data=document.metadata,
            ) for document in documents
        ]

    def simple_split_with_overlap(self, file_content: str) -> List[Chunk]:
        remaining_content_length = len(file_content)
        start_index = 0
        end_index = self._chunk_size + self._chunk_overlap
        chunks = list()
        while remaining_content_length > 0:
            new_slice = file_content[start_index:end_index]
            chunks.append(Chunk(content=new_slice))
            remaining_content_length = remaining_content_length - len(new_slice)
            start_index = start_index + len(new_slice) - self._chunk_overlap
            end_index = end_index + len(new_slice)
        return chunks

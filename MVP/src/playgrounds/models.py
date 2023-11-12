import dataclasses
from typing import List

OriginalFileID = str


@dataclasses.dataclass
class MatchingChunk:
    confidence: float
    content: str


@dataclasses.dataclass
class QueryResult:
    query: str
    matching_chunks: List[MatchingChunk]
    original_file: str

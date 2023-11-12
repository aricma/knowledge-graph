import dataclasses
from typing import List, Set, Any, Dict

import chromadb
from chromadb import QueryResult as ChromaQueryResult
from chromadb.api.models.Collection import Collection
from uuid import uuid4

from misc.utils import pprint


@dataclasses.dataclass
class Match:
    chunk_id: str
    content: str


@dataclasses.dataclass
class QueryResult:
    query: str
    match: Match
    distance: float


@dataclasses.dataclass
class Chunk:
    id: str
    content: str
    meta_data: Dict[str, Any]


class InMemoryChromaVectorDB:
    client: chromadb.Client
    ids: Set[str]
    max_amount_of_top_results: int = 3

    def __init__(self):
        self.client = chromadb.Client()
        self.ids = set()

    def add_chunks_to_collection(self, collection_name: str, chunks: List[Chunk]) -> None:
        collection = self._resolve_to_collection(collection_name)
        chunk_ids = [chunk.id for chunk in chunks]
        collection.add(
            # embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
            documents=[each.content for each in chunks],
            # add some dummy meta data to please chroma.add in case the meta data is an empty dict
            metadatas=[
                {
                    **each.meta_data,
                    "collection_name": collection_name,
                } for each in chunks
            ],
            ids=chunk_ids
        )
        for each in chunk_ids:
            self.ids.add(each)

    def query(self, collection_name: str, query: str) -> List[QueryResult]:
        collection = self._resolve_to_collection(collection_name)
        results = collection.query(
            query_texts=[query],
            n_results=self.max_amount_of_top_results
        )
        return self._to_result(results, query)

    def _resolve_to_collection(self, collection_name: str) -> Collection:
        all_collections = [each.name for each in self.client.list_collections()]
        if collection_name not in all_collections:
            self._add_collection(collection_name)
        return self._get_collection(collection_name)

    def _add_collection(self, collection_name: str) -> Collection:
        return self.client.create_collection(name=collection_name)

    def _get_collection(self, collection_name: str) -> Collection:
        return self.client.get_collection(name=collection_name)

    def _generate_id(self) -> str:
        generated_id = uuid4()
        while generated_id in self.ids:
            generated_id = uuid4()
        return str(generated_id)

    @staticmethod
    def _to_result(query_result: ChromaQueryResult, query: str) -> List[QueryResult]:
        return [
            QueryResult(
                query=query,
                match=Match(
                    chunk_id=chunk_id,
                    content=document,
                ),
                distance=distance,
            ) for chunk_id, distance, document in zip(
                query_result["ids"][0],
                query_result["distances"][0],
                query_result["documents"][0]
            )
        ]


if __name__ == '__main__':
    db = InMemoryChromaVectorDB()

    files = [
        "Honey Never Spoils: Archaeologists have discovered pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible. Honey's longevity can be attributed to its unique composition, which is naturally low in moisture and high in sugar, making it an inhospitable environment for bacteria and microorganisms. Additionally, honey is acidic and contains small amounts of hydrogen peroxide, which also inhibit growth of microbes.",
        "Octopuses Have Three Hearts: An octopus has a complex circulatory system with three hearts. Two of these hearts are responsible for pumping blood to the gills, while the third heart circulates it to the rest of the body. Interestingly, when an octopus swims, the heart that delivers blood to the body stops beating, which is why these creatures prefer crawling than swimming as it's less tiring.",
        "Bananas Are Berries, But Strawberries Aren't: In botanical terms, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh. Under this definition, bananas qualify as berries, but strawberries do not. Strawberries are actually considered 'aggregate fruits' because they form from a flower with multiple ovaries.",
        "The Eiffel Tower Can Grow: The Eiffel Tower in Paris, made of iron, can grow by up to six inches during the summer. When a substance is heated, its particles move more and it takes up a larger volume – this is known as thermal expansion. Conversely, the tower shrinks in the cold. Despite this expansion and contraction, the Eiffel Tower's height is officially listed as 324 meters (1,063 feet).",
        "Venus' Rotation: Venus is the only planet in the solar system that rotates clockwise on its axis. This is known as retrograde rotation and is quite unusual when compared to the rotation of most other planets. Additionally, a day on Venus (one complete rotation on its axis) is longer than a year on Venus (one complete orbit around the Sun).",
    ]

    db.add_chunks_to_collection("foo", [
        Chunk(
            id=str(uuid4()),
            content=file,
            meta_data={"meta": "data"}
        ) for file in files
    ])
    results = db.query("foo", "does honey spoil")
    print(pprint([dataclasses.asdict(each) for each in results]))

    results = db.query("foo", "is venus made of honey?")
    print(pprint([dataclasses.asdict(each) for each in results]))

    results = db.query("foo", "does venus rotate around honey?")
    print(pprint([dataclasses.asdict(each) for each in results]))

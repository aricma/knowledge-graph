from dataclasses import asdict
from pathlib import Path
from typing import List

from langchain.document_loaders import PyPDFLoader

from file_splitter.text_file_splitter import Chunk
from misc.utils import pprint


class PyPDFFileLoader:

    _temp_file_path: str

    def __init__(self, temp_directory: str):
        self._temp_file_path = temp_directory + "/temp_py_pdf_file_loader_file.pdf"
        Path(temp_directory).mkdir(
            parents=True,
            exist_ok=True,
            mode=0o777,
        )

    def load(self, file: bytes) -> List[Chunk]:
        self._get_file_path_for_url(file)
        loader = PyPDFLoader(
            file_path=self._temp_file_path,
            extract_images=True,
        )
        documents = loader.load()
        self._remove_temp_file()
        return [
            Chunk(
                content=document.page_content,
                meta_data=document.metadata,
            ) for document in documents
        ]

    def _get_file_path_for_url(self, file: bytes) -> None:
        with open(self._temp_file_path, "wb") as writer:
            writer.write(file)

    def _remove_temp_file(self) -> None:
        Path(self._temp_file_path).unlink()


if __name__ == '__main__':
    path_to_the_pdf_documents = Path(__file__).absolute().parent.parent.parent
    document_names = [
        "document_01.pdf",
        "document_02.pdf",
        "document_03.pdf",
    ]

    fl = PyPDFFileLoader(temp_directory=str(path_to_the_pdf_documents))
    chunks = list()
    for each in document_names:
        with open(path_to_the_pdf_documents / each, "rb") as reader:
            file = reader.read()
        chunks = chunks + fl.load(file)

    print(pprint([
        asdict(each)
        for each in chunks
    ]))

# if __name__ == '__main__':
#     import pdb
#     path_to_the_pdf_document = Path(__file__).absolute().parent.parent.parent / "document_01.pdf"
#     if not path_to_the_pdf_document.exists():
#         raise FileNotFoundError()
#     loader = PyPDFLoader(
#         file_path=str(path_to_the_pdf_document),
#         extract_images=True,
#     )
#     pages = loader.load()
#     pdb.set_trace()
#     print(pages)

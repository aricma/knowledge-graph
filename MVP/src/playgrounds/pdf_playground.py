from pathlib import Path

from misc.constants import TEMP_STORAGE_DIRECTORY_PATH, TEMP_FILE_LOADER_DIRECTORY_PATH
from playgrounds.file_adder import FileAdder
from playgrounds.utils import format_query_results

if __name__ == '__main__':
    fa = FileAdder(
        storage_directory=str(TEMP_STORAGE_DIRECTORY_PATH),
        file_loader_temp_directory=str(TEMP_FILE_LOADER_DIRECTORY_PATH),
    )

    path_to_the_pdf_documents = Path(__file__).absolute().parent
    document_names = [
        "document_01.pdf",
        "document_02.pdf",
        "document_03.pdf",
    ]

    added_files = list()

    for name in document_names:
        with open(path_to_the_pdf_documents / name, "rb") as reader:
            file = reader.read()
        added_files.append(fa.add_file(file=file, name=name))

    queries = [
        "How much did I spend on gorillas wear?",
        "When did I go over the speed limit?",
        "What is the address for Auto Hoffmann?",
    ]

    for query in queries:
        results = fa.query(query)
        print(format_query_results(results))

    # teardown
    for response in added_files:
        fa.remove_file(response.storage_id)

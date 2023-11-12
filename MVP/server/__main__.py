from contextlib import asynccontextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Union, List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import (
    HTMLResponse,
)

from misc.constants import TEMP_DIRECTORY_PATH
from playgrounds.file_adder import FileAdder

path_to_the_pdf_documents = Path(__file__).absolute().parent.parent
path_to_the_view = Path(__file__).absolute().parent.parent / "view/index.html"
path_to_storage = TEMP_DIRECTORY_PATH / "storage"
path_to_temp_file_loader = TEMP_DIRECTORY_PATH / "file_loader"
global_fa = FileAdder(
    storage_directory=str(path_to_storage),
    file_loader_temp_directory=str(path_to_temp_file_loader)
)

all_added_original_file_ids = list()


def setup() -> None:
    pass


def teardown() -> None:
    for each in all_added_original_file_ids:
        global_fa.remove_file(each)


@asynccontextmanager
async def lifespan():
    setup()
    yield
    teardown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    with open(path_to_the_view, "r") as reader:
        return HTMLResponse(
            content=reader.read()
        )


@app.post("/add-file")
async def add_file(files: List[UploadFile] = File(...)):
    for file in files:
        res = global_fa.add_file(file=file.file.read(), name=file.filename)
        all_added_original_file_ids.append(res.storage_id)
    return {
        "message": "Added files successfully."
    }


@app.get("/query")
async def query(q: Union[str, None] = None):
    results = global_fa.query(q)
    return {
        "results": [asdict(each) for each in results]
    }

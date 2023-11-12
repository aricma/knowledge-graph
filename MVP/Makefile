plain_text_playground:
	python src/playgrounds/plain_text_playground.py

pdf_playground:
	python src/playgrounds/pdf_playground.py

test_vector_db:
	python src/vector_db/in_memory_vector_db.py

test_file_storage:
	python src/file_storage/local_file_storage.py

test_file_splitter:
	python src/file_splitter/text_file_splitter.py

test_chunk_storage:
	python src/chunk_storage/sqlite_chunk_storage.py

test_py_pdf_file_loader:
	python src/file_loader/py_pdf_file_loader.py

.PHONY: server
server:
	uvicorn server.__main__:app --reload

server-reset:
	rm -rf ../.tmp

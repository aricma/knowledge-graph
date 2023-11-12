from pathlib import Path

TEMP_DIRECTORY_PATH = Path(__file__).absolute().parent.parent.parent.parent / ".tmp"
TEMP_STORAGE_DIRECTORY_PATH = TEMP_DIRECTORY_PATH / "storage"
TEMP_FILE_LOADER_DIRECTORY_PATH = TEMP_DIRECTORY_PATH / "file_loader"

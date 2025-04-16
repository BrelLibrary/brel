from brel.parsers.path_loaders.file_path_loader import FilePathLoader
from brel.parsers.path_loaders.folder_path_loader import FolderPathLoader
from brel.parsers.path_loaders.path_loader_resolver import PathLoaderResolver
from brel.parsers.path_loaders.zip_path_loader import ZipPathLoader


def create_path_loader_resolver() -> PathLoaderResolver:
    return PathLoaderResolver([FilePathLoader(), FolderPathLoader(), ZipPathLoader()])

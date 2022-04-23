import os

from pydantic import BaseSettings
CONFIG=None

class Settings(BaseSettings):
    root_path: str = os.getenv('ROOT_PATH', '') #os.path.dirname(os.path.realpath(__file__)))
    mnt_path: str = os.getenv('MNT_PATH', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mnt')) )
    temp_file_storage_path: str = os.getenv('TEMPORARY_FILE_STORAGE_PATH', os.path.join(mnt_path, "tmp"))

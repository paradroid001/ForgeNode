import os
import json

from pydantic import BaseSettings
from app.models.forgenode import ForgeNode
#CONFIG:ForgeNode=None

class Settings(BaseSettings):
    root_path: str = os.getenv('ROOT_PATH', '.') #os.path.dirname(os.path.realpath(__file__)))
    mnt_path: str = os.getenv('MNT_PATH', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mnt')) )
    temp_file_storage_path: str = os.getenv('TEMPORARY_FILE_STORAGE_PATH', os.path.join(mnt_path, "tmp"))
    config: ForgeNode = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_config()

    def load_config(self) -> ForgeNode:
        print("GET CONFIG WAS CALLED")
        if self.config is None:
            filepath = os.path.join(self.mnt_path, 'config.json')
            if os.path.exists(filepath):
                content = ""
                with open(filepath, "rb") as configfile:
                    content = configfile.read()
                self.config = ForgeNode(**json.loads(content))
            else:
                config = ForgeNode(name="Untitled")
                self.write_config()
                self.config = config
        return self.config

    def write_config(self):
        config_data = json.loads(self.config.json())
        filepath = os.path.join(self.mnt_path, 'config.json')
        with open(filepath, "w") as configfile:
            configfile.write(json.dumps(config_data, indent=4))

import os
import json
from app.settings import Settings
import app.settings as settings


def get_settings():
    """
    This dependency function is to allow settings to be overridden in testing via a FastAPI's dependency overrides
    method.
    """
    return Settings()

# CONFIG gets initialised once, and then never again
def get_config():
    if settings.CONFIG is None:
        filepath = os.path.join(get_settings().mnt_path, 'config.json')
        content = ""
        with open(filepath, "rb") as configfile:
            content = configfile.read()
            print(content)
        settings.CONFIG = json.loads(content)
    return settings.CONFIG

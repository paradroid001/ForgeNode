import os
import json
from app.settings import Settings
#import app.settings as settings
#from app.models.forgenode import ForgeNode


def get_settings():
    """
    This dependency function is to allow settings to be overridden in testing via a FastAPI's dependency overrides
    method.
    """
    return Settings()

# CONFIG gets initialised once, and then never again
# def get_config(settings) -> ForgeNode:
#    print("GET CONFIG WAS CALLED")
#    if settings.config is None:
#        filepath = os.path.join(settings.mnt_path, 'config.json')
#        if os.path.exists(filepath):
#            content = ""
#            with open(filepath, "rb") as configfile:
#                content = configfile.read()
#            settings.config = ForgeNode(**json.loads(content))
#        else:
#            config = ForgeNode(name="Untitled")
#            write_config(config, settings)
#            settings.config = config
#    print(settings.config)
#    return settings.config

# def write_config(config, settings):
#     config_data = json.loads(config.json())
#     print(config_data)
#     filepath = os.path.join(settings.mnt_path, 'config.json')
#     with open(filepath, "w") as configfile:
#         configfile.write(json.dumps(config_data, indent=4))

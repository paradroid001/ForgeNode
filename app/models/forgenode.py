import os
import json
from typing import TYPE_CHECKING, List, Optional, Dict, Union, Any
from enum import Enum
from pydantic import BaseModel, validator, Field

from app.models.env import Env, VirtualEnv
from app.settings import Settings
from app.dependencies import get_settings


def get_forgenode(settings: Settings = None):
    if settings is None:
        settings = get_settings()
    return ForgeNode.load(settings)


class ValueType(str, Enum):
    INT = "integer"
    FLOAT = "float"
    NUMBER = "number"
    STRING = "string"
    BOOL = "bool"


class PositionalValue(BaseModel):
    name: str
    value: Union[Any, None]
    value_type: ValueType

    def cmdline_str(self) -> str:
        if self.value is not None:
            return str(self.value)
        return ""


class FlaggedValue(PositionalValue):
    flag: str
    value: Optional[Union[Any, None]]
    value_type: Optional[ValueType]

    def cmdline_str(self) -> str:
        if self.value:
            return self.flag
        else:
            return ""
            # return f"{self.flag} {str(self.value)}"


class OutputValue(BaseModel):
    name: str
    value_type: ValueType


class ForgeTool(BaseModel):
    name: str
    root: Union[str, None]  # root dir
    command: str  # command to run
    env_name: Optional[str]  # env name, for lookup
    args: List[Union[PositionalValue, FlaggedValue]]  # args
    output: Union[OutputValue, None]
    description: Optional[str]

    env_cache: Optional[Union[VirtualEnv, Env]] = Field(
        exclude=True, default_factory=None)  # resolved env

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def env(self) -> Union[VirtualEnv, Env]:
        if self.env_cache is None and self.env_name is not None:
            self.env_cache = get_forgenode().get_env_by_name(self.env_name)
            print(f"tool got env: {self.env_cache}")
        return self.env_cache


class ForgeNode(BaseModel):
    name: str
    tools: Optional[Dict[str, ForgeTool]] = {}
    envs: Optional[Dict[str, Union[VirtualEnv, Env]]] = {}

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        smart_union = True  # check all unioned types for best match

    # def __init__(self, **kwargs):
    #    print("forgenode initing")
    #    super().__init__(**kwargs)
    @classmethod
    def load(cls, settings: Settings) -> 'ForgeNode':
        forgenode: ForgeNode = None
        print("GET CONFIG WAS CALLED")
        filepath = os.path.join(settings.mnt_path, 'config.json')
        if os.path.exists(filepath):
            content = ""
            with open(filepath, "rb") as configfile:
                content = configfile.read()
            forgenode = ForgeNode(**json.loads(content))
        else:
            forgenode = ForgeNode(name="Untitled")
            forgenode.save(settings)
        return forgenode

    def save(self, settings: Settings):
        config_data = json.loads(self.json())
        filepath = os.path.join(settings.mnt_path, 'config.json')
        with open(filepath, "w") as configfile:
            configfile.write(json.dumps(config_data, indent=4))

    def get_env_by_name(self, name: str):
        if name in self.envs:
            return self.envs[name]
        return None

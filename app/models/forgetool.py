from typing import List, Optional, Union, Any
from enum import Enum
from pydantic import BaseModel


class ValueType(str, Enum):
    INT = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"


class PositionalValue(BaseModel):
    name: str
    value: Union[Any | None]
    value_type: ValueType


class FlaggedValue(PositionalValue):
    flag: str
    value: Optional[Union[Any | None]]
    value_type: Optional[ValueType]


class OutputValue(BaseModel):
    name: str
    value_type: ValueType


class ForgeTool(BaseModel):
    name: str
    root: Union[str | None]  # root dir
    command: str  # command to run
    args: List[Union[PositionalValue | FlaggedValue]]  # args
    output: Union[OutputValue | None]
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

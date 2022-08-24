from typing import List
from pydantic import BaseModel

class ForgeTool(BaseModel):
    name: str
    root: str
    command: str
    args: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

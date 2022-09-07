from typing import List, Optional
from pydantic import BaseModel

class ForgeTool(BaseModel):
    name: str
    root: str # root dir
    command: str    #command to run
    args: List[str] #args
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

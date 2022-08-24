from typing import List, Optional, Dict
from pydantic import BaseModel


from app.models.forgetool import ForgeTool

class ForgeNode(BaseModel):
    name: str
    tools: Optional[Dict[str, ForgeTool]] = {}

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


    #def __init__(self, **kwargs):
    #    print("forgenode initing")
    #    super().__init__(**kwargs)
import os

from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Env(BaseModel):
    name: str
    env_vars: Dict[str, Any] = {}

    def cmdline_str(self) -> str:
        var_string = " ".join(
            [f'{key}={val}' for key, val in self.env_vars.items()])
        return var_string

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class VirtualEnv(Env):
    root: str
    python_bin: str = "python"

    def cmdline_str(self, tool_root: str = None) -> str:
        var_string = super().cmdline_str()
        root_dir = tool_root if tool_root is not None else ""
        return f". {os.path.join(root_dir, self.root, 'activate')}; {var_string}"

import os
import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Response, Depends, HTTPException
from starlette import status
from app.dependencies import get_settings  # , get_config, write_config
from app.utils.utils import execute_command
from app.settings import Settings

from app.models.forgetool import ForgeTool
from app.models.forgenode import ForgeNode

router = APIRouter(prefix="/tool")
#settings = get_settings()


@router.get("/all/")
async def read_config(settings: Settings = Depends(get_settings)):
    return settings.config


@router.get("/list/")
async def list_config(settings: Settings = Depends(get_settings)) -> List[ForgeTool]:
    tools: Dict[str:ForgeTool] = settings.config.tools
    print(tools)
    return [item for item in settings.config.tools.values()]


@router.post("/add/{tool_name}/")
async def add_tool(
        tool_name: str,
        tool_root_dir: str,
        tool_cmd: str,
        tool_args: Optional[List[str]],
        tool_description: Optional[str] = None,
        settings: Settings = Depends(get_settings)):
    thisnode: ForgeNode = settings.config
    tool = ForgeTool(name=tool_name, root=tool_root_dir,
                     command=tool_cmd, args=tool_args, description=tool_description)
    thisnode.tools[tool_name] = tool
    settings.write_config()


@router.patch("/edit/{tool_name}/")
async def edit_tool(
        tool_name: str,
        new_tool_name: Optional[str] = None,
        tool_root_dir: Optional[str] = None,
        tool_cmd: Optional[str] = None,
        tool_args: Optional[List[str]] = None,
        tool_description: Optional[str] = None,
        settings: Settings = Depends(get_settings)):
    if tool_name not in settings.config.tools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        tool = settings.config.tools[tool_name]
        if tool_root_dir is not None:
            tool.root = tool_root_dir
        if tool_cmd is not None:
            tool.command = tool_cmd
        if tool_args is not None:
            tool.args = tool_args
        if new_tool_name is not None:
            tool.name = new_tool_name
            settings.config.tools.pop(tool_name)  # pop old tool name
            settings.config.tools[new_tool_name] = tool
        if tool_description is not None:
            tool.description = tool_description
        settings.write_config()


@router.delete("/delete/")
async def delete_tool(
        tool_name: str,
        settings: Settings = Depends(get_settings)):
    if tool_name in settings.config.tools:
        del settings.config.tools[tool_name]
        settings.write_config()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{tool_name}/")
async def read_named_config(tool_name: str,
                            settings: Settings = Depends(get_settings)):
    if tool_name in settings.config.tools:
        return settings.config.tools[tool_name]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/run/{tool_name}/")
async def run_tool(tool_name: str,
                   settings: Settings = Depends(get_settings)):
    if tool_name not in settings.config.tools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tool {tool_name} not found")
    else:
        toolconfig: ForgeTool = settings.config.tools[tool_name]
        cmd = toolconfig.command
        f = cmd
        cwd = None
        if toolconfig.root is not None:
            print(f"mnt path is {settings.mnt_path}")
            cwd = os.path.join(settings.mnt_path,
                               toolconfig.root.replace("/mnt/", ""))
            f = os.path.join(cwd, cmd)
        print(f"tool cwd is {cwd}")

        args = toolconfig.args
        kwargs = {}

        # command = f"{f} {args}" #don't process args for now.
        command = f"{f}"
        print(f"The command was {command}")
        (proc, out, err) = await execute_command(command)
        print(out)
        print(err)
        # return Response({"out": out, "err": err}, status_code=status.HTTP_200_OK)
        return {"out": out, "err": err}

import os
import json
from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, Response, Depends, HTTPException
from starlette import status
from app.dependencies import get_settings  # , get_config, write_config
from app.utils.utils import execute_command
from app.settings import Settings

from app.models.forgenode import ForgeNode, ForgeTool, FlaggedValue, PositionalValue, OutputValue

router = APIRouter(prefix="/tool")
#settings = get_settings()


@router.get("/all/")
async def read_config(settings: Settings = Depends(get_settings)):
    return ForgeNode.load(settings)


@router.get("/list/")
async def list_config(settings: Settings = Depends(get_settings)) -> List[ForgeTool]:
    tools: Dict[str:ForgeTool] = ForgeNode.load(settings).tools
    print(tools)
    return [item for item in tools.values()]


@router.post("/add/{tool_name}/")
async def add_tool(
        tool_name: str,
        tool_root_dir: str,
        tool_cmd: str,
        tool_args: Optional[List[Union[PositionalValue | FlaggedValue]]],
        tool_output: Optional[Union[OutputValue | None]],
        tool_description: Optional[str] = None,
        settings: Settings = Depends(get_settings)):
    thisnode: ForgeNode = ForgeNode.load(settings)
    tool = ForgeTool(name=tool_name, root=tool_root_dir,
                     command=tool_cmd, args=tool_args, output=tool_output, description=tool_description)
    thisnode.tools[tool_name] = tool
    thisnode.save(settings)


@router.patch("/edit/{tool_name}/")
async def edit_tool(
        tool_name: str,
        new_tool_name: Optional[str] = None,
        tool_root_dir: Optional[str] = None,
        tool_cmd: Optional[str] = None,
        tool_args: Optional[List[Union[PositionalValue |
                                       FlaggedValue]]] = None,
        tool_output: Optional[Union[OutputValue | None]] = None,
        tool_description: Optional[str] = None,
        settings: Settings = Depends(get_settings)):
    forgenode = ForgeNode.load(settings)
    if tool_name not in forgenode.tools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        tool = forgenode.tools[tool_name]
        if tool_root_dir is not None:
            tool.root = tool_root_dir
        if tool_cmd is not None:
            tool.command = tool_cmd
        if tool_args is not None:
            tool.args = tool_args
        if tool_output is not None:
            tool.output = tool_output
        if new_tool_name is not None:
            tool.name = new_tool_name
            forgenode.tools.pop(tool_name)  # pop old tool name
            forgenode.tools[new_tool_name] = tool
        if tool_description is not None:
            tool.description = tool_description
        forgenode.save(settings)


@router.delete("/delete/")
async def delete_tool(
        tool_name: str,
        settings: Settings = Depends(get_settings)):
    forgenode = ForgeNode.load(settings)
    if tool_name in forgenode.tools:
        del forgenode.tools[tool_name]
        forgenode.save(settings)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{tool_name}/")
async def read_named_config(tool_name: str,
                            settings: Settings = Depends(get_settings)):
    forgenode = ForgeNode.load(settings)
    if tool_name in forgenode.tools:
        return forgenode.tools[tool_name]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/run/{tool_name}/")
async def run_tool(tool_name: str,
                   args: List[Union[FlaggedValue | PositionalValue]],
                   settings: Settings = Depends(get_settings)):
    forgenode = ForgeNode.load(settings)
    if tool_name not in forgenode.tools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tool {tool_name} not found")
    else:
        toolconfig: ForgeTool = forgenode.tools[tool_name]
        cmd = toolconfig.command
        f = cmd
        cwd = None
        if toolconfig.root is not None:
            print(f"mnt path is {settings.mnt_path}")
            cwd = os.path.join(settings.mnt_path,
                               toolconfig.root.replace("/mnt/", ""))
            f = os.path.join(cwd, cmd)
        print(f"tool cwd is {cwd}")
        print(f"tool args were {args}")
        args_str = ' '.join([arg.cmdline_str() for arg in args])
        print(f"tool args = {args_str}")
        command = f"{f} {args_str}"

        print(f"tool env is {toolconfig.env()}")
        if toolconfig.env() is not None:
            print(f"tool env = {toolconfig.env().cmdline_str(cwd)}")
            command = f"{toolconfig.env().cmdline_str(cwd)}{command}"
        print(f"The command was {command}")
        (proc, out, err) = await execute_command(command)
        print(out)
        print(err)
        # return Response({"out": out, "err": err}, status_code=status.HTTP_200_OK)
        return {"out": out, "err": err}

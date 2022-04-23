import os
import json
from typing import List, Dict, Any
from fastapi import APIRouter, Response, Depends, HTTPException
from starlette import status
from app.dependencies import get_settings, get_config
from app.utils.utils import execute_command

router = APIRouter(prefix="/tool")
settings = get_settings()

@router.get("/all/")
async def read_config():
    #filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    #filepath = os.path.join(settings.root_path, '../mnt/')
    return get_config()

@router.get("/{name}")
async def read_named_config(name:str):
    config = get_config()
    if name in config:
        return config[name]
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/{name}/run")
async def run_tool(name:str, config=Depends(get_config), settings=Depends(get_settings)):
    if name in config:
        toolconfig = config[name]
        cwd = os.path.join(settings.mnt_path, toolconfig["dir"].replace("/mnt/", ""))
        cmd = toolconfig["cmd"]
        args = toolconfig["args"]
        kwargs = {}
        f = os.path.join(cwd, args[0])
        command = f"{cmd} {f}"
        print(f"The command was {command}")
        (proc, out, err) = await execute_command(command)
        print(out)
        print(err)
        #return Response({"out": out, "err": err}, status_code=status.HTTP_200_OK)
        return {"out": out, "err": err}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tool {name} not found")
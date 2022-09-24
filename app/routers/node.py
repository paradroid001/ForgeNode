from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, Response, Depends, HTTPException
from starlette import status
from app.dependencies import get_settings
from app.settings import Settings
from app.utils.utils import get_ram_load, get_system_load
from app.models.env import Env, VirtualEnv
from app.models.forgenode import ForgeNode

router = APIRouter(prefix="")


@router.get("/stats/")
async def get_stats(settings: Settings = Depends(get_settings)):
    return {'cpu': get_system_load(), 'mem': get_ram_load()}


@router.get("/env/{name}/")
async def get_env(name: str, settings=Depends(get_settings)):
    forgenode: ForgeNode = ForgeNode.load(settings)
    print(forgenode)
    for env_name in forgenode.envs:
        if env_name == name:
            return forgenode.envs[env_name]
    return None


@router.post("/env/new/")
async def add_env(env: Union[VirtualEnv, Env], settings=Depends(get_settings)):
    forgenode: ForgeNode = ForgeNode.load(settings)
    forgenode.envs[env.name] = env
    # settings.write_config()
    forgenode.save(settings)


@router.patch("/env/edit/")
async def edit_env(env: Union[VirtualEnv, Env], settings=Depends(get_settings)):
    forgenode: ForgeNode = ForgeNode.load(settings)
    if name in forgenode.envs:
        forgenode.envs[name] = env
        # settings.write_config()
        forgenode.save(settings)

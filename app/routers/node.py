from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Response, Depends, HTTPException
from starlette import status
from app.dependencies import get_settings
from app.settings import Settings
from app.utils.utils import get_ram_load, get_system_load

router = APIRouter(prefix="")


@router.get("/stats/")
async def get_stats(settings: Settings = Depends(get_settings)):
    return {'cpu': get_system_load(), 'mem': get_ram_load()}

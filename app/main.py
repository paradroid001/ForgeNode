from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.dependencies import get_settings
from app.routers import tool

settings = get_settings()

app = FastAPI(root_path=settings.root_path)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

#router = APIRouter()
#app.router = router
app.include_router(tool.router)

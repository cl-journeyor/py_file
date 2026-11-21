from fastapi import APIRouter, FastAPI
from utils import consts

app = FastAPI(
    docs_url=None,
    redoc_url=None
)
router = APIRouter()

try:
    router.frontend('/', directory='dist')
    app.include_router(router)
except RuntimeError:
    pass

consts.FILES_DIR.mkdir(exist_ok=True)

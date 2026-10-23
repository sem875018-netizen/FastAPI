import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import engine, Base
from models.user import User  # noqa: F401 — регистрирует модель в metadata
from models.snippet import Snippet  # noqa: F401
from api.auth import router as auth_router
from api.snippets import router as snippets_router

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Application started; database tables are ready")
    yield
    await engine.dispose()
    logger.info("Application stopped")


app = FastAPI(title="Code Snippets API", version="1.0.0", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(snippets_router)


@app.get("/", tags=["health"])
async def healthcheck():
    return {"status": "ok"}

import uvicorn
from fastapi import FastAPI
from app.db.connections import engine
from app.video.model import Base
from app.video.routers import router
from logging_config import setup_logging


setup_logging()

app = FastAPI(
    title="Video Management API",
    description="REST API для работы с базой данных видео",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "Video API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

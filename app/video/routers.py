from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db
from app.video import schemas, crud
from app.video.model import VideoStatus

import logging


router = APIRouter(prefix="/videos", tags=["videos"])
logger = logging.getLogger("app.routers.videos")


@router.post("", response_model=schemas.VideoRead)
async def create_video(
    data: schemas.VideoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Добавление нового видео.
    Статус по умолчанию: "new"
    """
    try:
        logger.info("Creating video with data: %s", data.model_dump())
        video = await crud.create_video(db, data.model_dump())
        logger.info("Video created with id=%s", video.id)
        return video
    except Exception:
        logger.exception("Failed to create video")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("", response_model=list[schemas.VideoRead])
async def list_videos(
    db: Annotated[AsyncSession, Depends(get_db)],
    status: Annotated[list[VideoStatus] | None, Query()] = None,
    camera_number: Annotated[list[int] | None, Query()] = None,
    location: Annotated[list[str] | None, Query()] = None,
    start_time_from: datetime | None = None,
    start_time_to: datetime | None = None,
):
    """
    Получение списка видео с возможностью фильтрации по:
    - статусу
    - номеру камеры
    - локации
    - времени начала записи
    """
    try:
        filters = {
            "status": status,
            "camera_number": camera_number,
            "location": location,
            "start_time_from": start_time_from,
            "start_time_to": start_time_to,
        }
        logger.info("Listing videos with filters: %s", filters)
        videos = await crud.get_videos(
            session=db,
            status=status,
            camera_number=camera_number,
            location=location,
            start_time_from=start_time_from,
            start_time_to=start_time_to,
        )
        logger.info("Returned %d videos", len(videos))
        return videos
    except Exception:
        logger.exception("Failed to list videos")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{video_id}", response_model=schemas.VideoRead)
async def get_video(
    video_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Получение информации о видео по ID
    """
    try:
        video = await crud.get_video_by_id(db, video_id)
        if not video:
            logger.warning("Video not found: id=%s", video_id)
            raise HTTPException(status_code=404, detail="Video not found")
        logger.info("Fetched video id=%s", video_id)
        return video
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to fetch video id=%s", video_id)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch("/{video_id}/status", response_model=schemas.VideoRead)
async def update_video_status(
    video_id: int,
    data: schemas.VideoStatusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Обновление статуса видео.
    Допустимые статусы: "new", "transcoded", "recognized"
    """
    try:
        video = await crud.get_video_by_id(db, video_id)
        if not video:
            logger.warning("Video not found for status update: id=%s", video_id)
            raise HTTPException(status_code=404, detail="Video not found")

        old_status = video.status
        video = await crud.update_video_status(db, video, data.status)
        logger.info(
            "Updated video id=%s status: %s -> %s", video_id, old_status, data.status
        )
        return video
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to update status for video id=%s", video_id)
        raise HTTPException(status_code=500, detail="Internal Server Error")

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db
from app.video import schemas, crud
from app.video.model import VideoStatus

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("", response_model=schemas.VideoRead)
async def create_video(
    data: schemas.VideoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Добавление нового видео.
    Статус по умолчанию: "new"
    """
    return await crud.create_video(db, data.model_dump())


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
    return await crud.get_videos(
        session=db,
        status=status,
        camera_number=camera_number,
        location=location,
        start_time_from=start_time_from,
        start_time_to=start_time_to,
    )


@router.get("/{video_id}", response_model=schemas.VideoRead)
async def get_video(
    video_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Получение информации о видео по ID
    """
    video = await crud.get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


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
    video = await crud.get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return await crud.update_video_status(db, video, data.status)
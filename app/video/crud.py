from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.video.model import Video, VideoStatus


async def create_video(
    session: AsyncSession,
    data: dict,
) -> Video:
    video = Video(**data)
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


async def get_video_by_id(
    session: AsyncSession,
    video_id: int,
) -> Video | None:
    result = await session.execute(select(Video).where(Video.id == video_id))
    return result.scalar_one_or_none()


async def get_videos(
    session: AsyncSession,
    status: list[VideoStatus] | None = None,
    camera_number: list[int] | None = None,
    location: list[str] | None = None,
    start_time_from: datetime | None = None,
    start_time_to: datetime | None = None,
) -> Sequence[Video]:
    stmt = select(Video)

    if status:
        stmt = stmt.where(Video.status.in_(status))
    if camera_number:
        stmt = stmt.where(Video.camera_number.in_(camera_number))
    if location:
        stmt = stmt.where(Video.location.in_(location))
    if start_time_from:
        stmt = stmt.where(Video.start_time >= start_time_from)
    if start_time_to:
        stmt = stmt.where(Video.start_time <= start_time_to)

    result = await session.execute(stmt)
    return result.scalars().all()


async def update_video_status(
    session: AsyncSession,
    video: Video,
    status: VideoStatus,
) -> Video:
    video.status = status
    await session.commit()
    await session.refresh(video)
    return video

from datetime import datetime, timedelta
from typing import Annotated

from pydantic import BaseModel, Field

from app.video.model import VideoStatus


class VideoCreate(BaseModel):
    video_path: Annotated[str, Field(min_length=1)]
    start_time: datetime
    duration: Annotated[timedelta, Field(gt=timedelta(0))]
    camera_number: Annotated[int, Field(gt=0)]
    location: Annotated[str, Field(min_length=1)]


class VideoRead(VideoCreate):
    id: int
    status: VideoStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class VideoStatusUpdate(BaseModel):
    status: VideoStatus

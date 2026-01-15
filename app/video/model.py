from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Interval,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class VideoStatus(str, Enum):
    new = "new"
    transcoded = "transcoded"
    recognized = "recognized"


class Video(Base):
    __tablename__ = "videos"

    __table_args__ = (
        CheckConstraint("camera_number > 0", name="camera_number_positive"),
        CheckConstraint("duration > interval '0'", name="duration_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    video_path: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[timedelta] = mapped_column(Interval, nullable=False)
    camera_number: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[VideoStatus] = mapped_column(
        nullable=False,
        default=VideoStatus.new,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
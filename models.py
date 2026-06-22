from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    analyses = relationship(
        "Analysis",
        back_populates="user"
    )

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    youtube_video_id = Column(
        String,
        unique=True,
        nullable=False
    )
    title = Column(String, nullable=True)
    channel_name = Column(
        String,
        nullable=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    analyses = relationship(
        "Analysis",
        back_populates="video"
    )

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    video_id = Column(
        Integer,
        ForeignKey("videos.id"),
        nullable=False
    )
    toxicity_score = Column(
        Float,
        nullable=True
    )
    engagement_score = Column(
        Float,
        nullable=True
    )
    sentiment_summary = Column(
        JSON,
        nullable=True
    )
    emotion_summary = Column(
        JSON,
        nullable=True
    )
    analysis_json = Column(
        JSON,
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    user = relationship(
        "User",
        back_populates="analyses"
    )
    video = relationship(
        "Video",
        back_populates="analyses"
    )
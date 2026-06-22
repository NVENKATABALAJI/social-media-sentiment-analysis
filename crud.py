from sqlalchemy.orm import Session

from models import Video, Analysis

from models import User

from sqlalchemy import func


def get_video_by_youtube_id(
    db: Session,
    youtube_video_id: str
):
    return (
        db.query(Video)
        .filter(
            Video.youtube_video_id == youtube_video_id
        )
        .first()
    )


def create_video(
    db: Session,
    youtube_video_id: str,
    title: str = None,
    channel_name: str = None
    ):
    video = Video(
        youtube_video_id=youtube_video_id,
        title=title,
        channel_name=channel_name
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video


def create_analysis(
    db: Session,
    user_id: int,
    video_id: int,
    engagement_score: float,
    sentiment_summary: dict,
    emotion_summary: dict,
    analysis_json: dict
):
    analysis = Analysis(
        user_id=user_id,
        video_id=video_id,
        engagement_score=engagement_score,
        sentiment_summary=sentiment_summary,
        emotion_summary=emotion_summary,
        analysis_json=analysis_json
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis

def update_video_metadata(
    db: Session,
    video: Video,
    title: str,
    channel_name: str
):
    video.title = title
    video.channel_name = channel_name

    db.commit()
    db.refresh(video)

    return video

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(
    db: Session,
    email: str,
    username: str,
    password_hash: str
):
    user = User(
        email=email,
        username=username,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def get_user_analyses(
    db: Session,
    user_id: int
):
    return (
        db.query(
            Analysis,
            Video
        )
        .join(
            Video,
            Analysis.video_id == Video.id
        )
        .filter(
            Analysis.user_id == user_id
        )
        .order_by(
            Analysis.created_at.desc()
        )
        .all()
    )

def get_analysis_by_id(
    db: Session,
    analysis_id: int,
    user_id: int
):
    return (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id,
            Analysis.user_id == user_id
        )
        .first()
    )

def delete_analysis(
    db: Session,
    analysis_id: int,
    user_id: int
):
    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id,
            Analysis.user_id == user_id
        )
        .first()
    )

    if not analysis:
        return None

    db.delete(analysis)
    db.commit()

    return True

def get_dashboard_stats(
    db: Session,
    user_id: int
):
    analyses = (
        db.query(Analysis)
        .filter(
            Analysis.user_id == user_id
        )
        .all()
    )

    total_analyses = len(analyses)

    if total_analyses == 0:
        return {
            "total_analyses": 0,
            "unique_videos": 0,
            "average_engagement_score": 0,
            "latest_analysis": None
        }

    unique_videos = len(
        set(
            a.video_id
            for a in analyses
        )
    )

    avg_engagement = round(
        sum(
            a.engagement_score or 0
            for a in analyses
        ) / total_analyses,
        2
    )

    latest_analysis = max(
        a.created_at
        for a in analyses
    )

    return {
        "total_analyses": total_analyses,
        "unique_videos": unique_videos,
        "average_engagement_score": avg_engagement,
        "latest_analysis": latest_analysis
    }
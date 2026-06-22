from fastapi import FastAPI, HTTPException
from transformers import pipeline
from googleapiclient.discovery import build
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import os
import re
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from crud import (
    get_video_by_youtube_id,
    create_video,
    create_analysis
)

from crud import (
    get_video_by_youtube_id,
    create_video,
    create_analysis,
    update_video_metadata
)

from schemas import (
    UserCreate,
    UserLogin,
    UserResponse
)

from security import hash_password

from crud import (
    get_user_by_email,
    get_user_by_username,
    create_user
)

from security import (
    hash_password,
    verify_password
)

from crud import authenticate_user

from security import (
    hash_password,
    verify_password,
    create_access_token
)

from security import get_current_user

from fastapi.security import OAuth2PasswordRequestForm

from crud import get_user_analyses

from crud import get_analysis_by_id

from crud import delete_analysis

from crud import get_dashboard_stats

load_dotenv()

app = FastAPI()

# ------------------ MODELS ------------------

classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ API KEY ------------------

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("❌ Missing YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ------------------ HELPERS ------------------

def clean_comment(text):
    return re.sub(r"<.*?>", "", text)

def detect_language(text):
    text = text.lower()

    if any('\u0C00' <= ch <= '\u0C7F' for ch in text):
        return "Telugu"
    if any('\u0900' <= ch <= '\u097F' for ch in text):
        return "Hindi"

    if re.search(r'[a-zA-Z]', text):
        local_words = ["ra", "bro", "anna", "bhai", "da", "lo", "ki"]
        if any(word in text for word in local_words):
            return "Code-Mixed"
        return "English"

    return "Unknown"

ASPECT_KEYWORDS = {
    "Audio": ["audio", "sound", "voice", "music", "dubbing", "bgm"],
    "Video": ["video", "visual", "editing", "vfx", "graphics"],
    "Story": ["story", "plot", "script", "scene"],
    "Acting": ["acting", "actor", "performance"],
    "Release": ["release", "date", "when"],
    "General": []
}

def detect_aspects(comment):
    comment = comment.lower()
    aspects = []
    for aspect, keywords in ASPECT_KEYWORDS.items():
        if any(word in comment for word in keywords):
            aspects.append(aspect)
    return aspects if aspects else ["General"]

def detect_sarcasm(text):
    text_lower = text.lower()
    return any(p in text_lower for p in ["lol", "as if", "yeah right"])

def batch_process(model, texts, batch_size=10):
    results = []
    for i in range(0, len(texts), batch_size):
        results.extend(model(texts[i:i+batch_size]))
    return results
# ------------------ ENGAGEMENT PREDICTION ------------------

def calculate_engagement(sentiment_counts, total_comments, toxicity_list, trend_data):

    positive = sentiment_counts["Positive"]
    negative = sentiment_counts["Negative"]

    pos_ratio = positive / total_comments
    neg_ratio = negative / total_comments

    # Toxicity ratio
    toxic_count = sum(toxicity_list)
    toxic_ratio = toxic_count / total_comments

    # Trend growth (last vs first)
    growth = trend_data[-1]["positive"] - trend_data[0]["positive"]

    # Engagement Score (0–100)
    score = (
        pos_ratio * 50 +
        (1 - neg_ratio) * 20 +
        (1 - toxic_ratio) * 15 +
        (growth / total_comments) * 15
    ) * 100

    score = round(min(score, 100), 2)

    # Virality Prediction
    if score > 70:
        virality = "High 🚀"
    elif score > 40:
        virality = "Medium ⚡"
    else:
        virality = "Low ⚠️"

    # Risk Detection
    if toxic_ratio > 0.2 or neg_ratio > 0.3:
        risk = "High 🔴"
    elif toxic_ratio > 0.1:
        risk = "Medium 🟠"
    else:
        risk = "Low 🟢"

    # Insight Summary
    if virality.startswith("High") and risk.startswith("Low"):
        insight = "Strong positive engagement with healthy audience response"
    elif risk.startswith("High"):
        insight = "Potential backlash detected due to negativity/toxicity"
    else:
        insight = "Moderate engagement with mixed audience reaction"

    return score, virality, risk, insight

# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"message": "YouTube Sentiment API running 🚀"}


@app.post(
    "/register",
    response_model=UserResponse
)

def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_email = get_user_by_email(
        db,
        user.email
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = get_user_by_username(
        db,
        user.username
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = create_user(
        db=db,
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )

    return new_user

@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(
        db,
        form_data.username
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
            form_data.password,
            db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/history")
def get_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    records = get_user_analyses(
        db,
        current_user.id
    )

    history = []

    for analysis, video in records:

        history.append({
            "analysis_id": analysis.id,
            "video_title": video.title,
            "youtube_video_id": video.youtube_video_id,
            "engagement_score": analysis.engagement_score,
            "created_at": analysis.created_at
        })

    return history

@app.get("/history/{analysis_id}")
def get_analysis_details(
    analysis_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    analysis = get_analysis_by_id(
        db,
        analysis_id,
        current_user.id
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return analysis.analysis_json

@app.delete("/history/{analysis_id}")
def delete_analysis_endpoint(
    analysis_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    deleted = delete_analysis(
        db,
        analysis_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return {
        "message": "Analysis deleted successfully"
    }

@app.get("/dashboard/stats")
def dashboard_stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_dashboard_stats(
        db,
        current_user.id
    )

@app.get("/analyze/{video_id}")
def analyze_video(
    video_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    video_items = video_response.get("items", [])

    if not video_items:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    video_snippet = video_items[0]["snippet"]

    video_title = video_snippet["title"]

    channel_name = video_snippet["channelTitle"]

    try:
        comments = []

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50
        )

        response = request.execute()

        for item in response.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(clean_comment(text))

        if not comments:
            raise HTTPException(status_code=404, detail="No comments found")

        # -------- MODELS --------
        predictions = batch_process(classifier, comments)
        emotion_predictions = batch_process(emotion_classifier, comments)
        toxicity_predictions = batch_process(toxicity_classifier, comments)

        # -------- CLUSTERING --------
        embeddings = embedding_model.encode(comments)
        kmeans = KMeans(n_clusters=4, random_state=42)
        labels = kmeans.fit_predict(embeddings)

        sentiment_map = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }

        emotion_map = {
            "joy": "Joy 😊",
            "anger": "Anger 😡",
            "sadness": "Sadness 😢",
            "fear": "Fear 😨",
            "surprise": "Surprise 😲",
            "disgust": "Disgust 🤢",
            "neutral": "Neutral 😐"
        }

        detailed_results = []
        counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        emotion_counts = {}
        language_counts = {}
        toxicity_list = []
        aspect_summary = {}

        trend_data = []
        pos = neu = neg = 0

        for i, (text, pred, emo) in enumerate(zip(comments, predictions, emotion_predictions)):

            sentiment = sentiment_map[pred["label"]]
            emotion = emotion_map.get(emo["label"], emo["label"])

            language = detect_language(text)
            aspects = detect_aspects(text)
            sarcasm = detect_sarcasm(text)

            tox = toxicity_predictions[i]
            is_toxic = tox["label"] == "toxic" and tox["score"] > 0.6
            toxicity_list.append(1 if is_toxic else 0)

            if sarcasm and sentiment == "Positive":
                sentiment = "Negative"

            counts[sentiment] += 1
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            language_counts[language] = language_counts.get(language, 0) + 1

            for a in aspects:
                if a not in aspect_summary:
                    aspect_summary[a] = {"Positive": 0, "Neutral": 0, "Negative": 0}
                aspect_summary[a][sentiment] += 1

            # -------- TREND --------
            if sentiment == "Positive":
                pos += 1
            elif sentiment == "Neutral":
                neu += 1
            else:
                neg += 1

            trend_data.append({
                "time": i,
                "positive": pos,
                "neutral": neu,
                "negative": neg
            })

            # ✅ CLUSTER ADD
            cluster_id = int(labels[i])

            detailed_results.append({
                "comment": text,
                "sentiment": sentiment,
                "emotion": emotion,
                "language": language,
                "aspects": aspects,
                "sarcasm": sarcasm,
                "toxic": is_toxic,
                "cluster": cluster_id,   # 🔥 NEW
                "score": round(pred["score"], 3)
            })

        # -------- CLUSTER SUMMARY --------
        cluster_summary = {}

        for c in detailed_results:
            cid = c["cluster"]

            if cid not in cluster_summary:
                cluster_summary[cid] = {
                    "count": 0,
                    "sample_comments": []
                }

            cluster_summary[cid]["count"] += 1

            if len(cluster_summary[cid]["sample_comments"]) < 3:
                cluster_summary[cid]["sample_comments"].append(c["comment"])

        total = len(detailed_results)

        engagement_score, virality_prediction, risk_alert, insight_summary = calculate_engagement(
            counts,
            total,
            toxicity_list,
            trend_data
        )

        percentages = {
            k: round(v / total * 100, 2)
            for k, v in counts.items()
        }

        result = {
            "video_id": video_id,
            "total_comments": total,
            "sentiment_counts": counts,
            "sentiment_percentages": percentages,
            "emotion_counts": emotion_counts,
            "aspect_summary": aspect_summary,
            "language_distribution": language_counts,
            "trend_data": trend_data,
            "engagement_score": engagement_score,
            "virality_prediction": virality_prediction,
            "risk_alert": risk_alert,
            "insight_summary": insight_summary,
            "clusters": cluster_summary,
            "detailed_comments": detailed_results
        }
        video = get_video_by_youtube_id(
            db,
            video_id
        )

        if not video:
            video = create_video(
                db=db,
                youtube_video_id=video_id,
                title=video_title,
                channel_name=channel_name
            )
        else:
            if not video.title or not video.channel_name:
                update_video_metadata(
                    db=db,
                    video=video,
                    title=video_title,
                    channel_name=channel_name
                )

        create_analysis(
            db=db,
            user_id=current_user.id,
            video_id=video.id,
            engagement_score=engagement_score,
            sentiment_summary=counts,
            emotion_summary=emotion_counts,
            analysis_json=result
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/me")
def get_me(
    current_user = Depends(
        get_current_user
    )
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }
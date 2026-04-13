from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    TaskRequest,
    TaskResponse,
    DashboardStats,
)
from app.models import User
from app.crud import (
    create_user,
    get_user_by_username,
    create_task,
    update_task_status,
    get_all_tasks,
    get_dashboard_stats,
)
from app.auth import verify_password, create_access_token
from app.dependencies import get_current_user
from app.agents.ceo_agent import ceo_agent
from app.notifications import send_email_notification, send_whatsapp_notification


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Agent AI Enterprise Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Enterprise multi-agent backend running"}


@app.post("/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = create_user(db, payload.username, payload.email, payload.password)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
    }


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, payload.username)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
    }


@app.get("/dashboard/stats", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = get_dashboard_stats(db)

    if stats is None:
        raise HTTPException(status_code=500, detail="Dashboard stats not returned")

    return stats


@app.get("/agent/history", response_model=List[TaskResponse])
def agent_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = get_all_tasks(db)

    if tasks is None:
        return []

    return tasks


@app.post("/agent/run", response_model=TaskResponse)
def run_agent(
    payload: TaskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = create_task(
        db=db,
        goal=payload.goal,
        department="CEO",
        assigned_agent="Router",
        owner_id=current_user.id,
        notification_email=payload.notification_email,
        notification_whatsapp=payload.notification_whatsapp,
    )

    try:
        task = update_task_status(db, task.id, "running")

        response = ceo_agent(payload.goal)

        task = update_task_status(
            db,
            task.id,
            response.get("status", "completed"),
            response.get("result", "No result"),
        )

        return task

    except Exception as e:
        print("ERROR:", e)

        task = update_task_status(db, task.id, "failed", str(e))

        return task

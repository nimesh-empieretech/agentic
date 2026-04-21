from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models import AgentTask

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
from langchain_openrouter import ChatOpenRouter

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
    return {"message": "multi-agent backend running"}


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
    tasks = (
        db.query(AgentTask)
        .filter(AgentTask.owner_id == current_user.id)
        .order_by(AgentTask.id.asc())  # ✅ reverse order (old → new)
        .all()
    )

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
        notification_email=getattr(payload, "notification_email", None),
        notification_whatsapp=getattr(payload, "notification_whatsapp", None),
    )

    response = {
        "status": "failed",
        "result": "Unknown error",
        "department": "CEO",
        "assigned_agent": "Router",
        "action": None,
        "app": None,
        "url": None,
    }

    try:
        task = update_task_status(
            db=db,
            task_id=task.id,
            status_value="running",
        )

        response = ceo_agent(payload.goal)

        task = update_task_status(
            db=db,
            task_id=task.id,
            status_value=response.get("status", "completed"),
            result=response.get("result", "No result"),
            department=response.get("department", "CEO"),
            assigned_agent=response.get("assigned_agent", "Router"),
        )

    except Exception as e:
        task = update_task_status(
            db=db,
            task_id=task.id,
            status_value="failed",
            result=str(e),
        )
        response["result"] = str(e)

    return {
        "id": task.id,
        "goal": task.goal,
        "department": task.department,
        "assigned_agent": task.assigned_agent,
        "result": task.result,
        "status": task.status,
        "owner_id": task.owner_id,
        "notification_email": task.notification_email,
        "notification_whatsapp": task.notification_whatsapp,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "action": response.get("action"),
        "app": response.get("app"),
        "url": response.get("url"),
    }

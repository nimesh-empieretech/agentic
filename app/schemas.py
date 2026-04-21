from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TaskRequest(BaseModel):
    goal: str
    notification_email: Optional[EmailStr] = None
    notification_whatsapp: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    goal: str
    department: str
    assigned_agent: str
    result: str
    status: str
    created_at: datetime

    action: Optional[str] = None
    app: Optional[str] = None
    url: Optional[str] = None

    class Config:
        from_attributes = True


class TaskUpdateStatus(BaseModel):
    status: str


class DashboardStats(BaseModel):
    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int

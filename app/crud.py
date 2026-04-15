from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, AgentTask
from app.auth import hash_password


def create_user(db: Session, username: str, email: str, password: str):
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_task(
    db: Session,
    goal: str,
    department: str,
    assigned_agent: str,
    owner_id: int = None,
    notification_email: str = None,
    notification_whatsapp: str = None,
):
    task = AgentTask(
        goal=goal,
        department=department,
        assigned_agent=assigned_agent,
        status="pending",
        owner_id=owner_id,
        notification_email=notification_email,
        notification_whatsapp=notification_whatsapp,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task_status(
    db: Session,
    task_id: int,
    status_value: str,
    result: str = None,
    department: str = None,
    assigned_agent: str = None,
):
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        return None

    task.status = status_value

    if result is not None:
        task.result = result

    if department is not None:
        task.department = department

    if assigned_agent is not None:
        task.assigned_agent = assigned_agent

    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int):
    return db.query(AgentTask).filter(AgentTask.id == task_id).first()


def get_all_tasks(db: Session):
    return db.query(AgentTask).order_by(AgentTask.id.desc()).all()


def get_dashboard_stats(db: Session):
    total = db.query(func.count(AgentTask.id)).scalar() or 0
    pending = (
        db.query(func.count(AgentTask.id))
        .filter(AgentTask.status == "pending")
        .scalar()
        or 0
    )
    running = (
        db.query(func.count(AgentTask.id))
        .filter(AgentTask.status == "running")
        .scalar()
        or 0
    )
    completed = (
        db.query(func.count(AgentTask.id))
        .filter(AgentTask.status == "completed")
        .scalar()
        or 0
    )
    failed = (
        db.query(func.count(AgentTask.id)).filter(AgentTask.status == "failed").scalar()
        or 0
    )

    return {
        "total_tasks": total,
        "pending_tasks": pending,
        "running_tasks": running,
        "completed_tasks": completed,
        "failed_tasks": failed,
    }

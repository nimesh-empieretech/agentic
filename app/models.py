from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("AgentTask", back_populates="owner")


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    assigned_agent = Column(String(100), nullable=False)
    result = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    notification_email = Column(String(150), nullable=True)
    notification_whatsapp = Column(String(30), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    department = Column(String(100))
    message = Column(Text)
    keywords = Column(Text)  # 🔥 important
    is_active = Column(Boolean, default=True)


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    department = Column(String(100))

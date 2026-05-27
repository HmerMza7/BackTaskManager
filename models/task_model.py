from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Priority(Base):
    __tablename__ = "priority"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    level = Column(String(255), nullable=False)

class StateTask(Base):
    __tablename__ = "state_task"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    state = Column(String(255), nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    state_id = Column(BigInteger, ForeignKey("state_task.id"), default=1)
    priority_id = Column(BigInteger, ForeignKey("priority.id"))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(BigInteger, ForeignKey("users.id"))

    state = relationship("StateTask")
    priority = relationship("Priority")

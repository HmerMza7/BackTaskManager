from sqlalchemy.orm import Session
from models.task_model import Task
from fastapi import HTTPException, status


class TaskController:
    @staticmethod
    def create_task(db: Session, task_data: dict):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            state_id=task_data.get("state_id", 1),
            priority_id=task_data.get("priority_id"),
            user_id=task_data.get("user_id"),
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {
            "message": "Task created successfully",
            "task": new_task,
        }

    @staticmethod
    def get_tasks(db: Session, user_id: int = None):
        query = db.query(Task)

        if user_id:
            query = query.filter(Task.user_id == user_id)

        return query.all()

    @staticmethod
    def update_task(db: Session, task_id: int, task_data: dict):
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        for key, value in task_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return {"message": "Task updated successfully", "task": task}

    @staticmethod
    def delete_task(db: Session, task_id: int):
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}

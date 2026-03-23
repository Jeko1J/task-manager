from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas
from app.routers import tasks
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(tasks.router)


@app.get("/")
async def home(request: Request, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Главная страница со списком задач"""
    if status and status != "все":
        query = db.query(models.Task).filter(models.Task.status == status)
    else:
        query = db.query(models.Task)

    tasks = query.order_by(models.Task.created_at.desc()).all()

    total_tasks = db.query(models.Task).count()
    new_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.NEW).count()
    in_progress_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.IN_PROGRESS).count()
    completed_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.COMPLETED).count()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "current_status": status or "все",
            "stats": {
                "total": total_tasks,
                "new": new_tasks,
                "in_progress": in_progress_tasks,
                "completed": completed_tasks
            }
        }
    )


@app.get("/tasks/new")
async def create_task_form(request: Request):
    """Форма создания новой задачи"""
    return templates.TemplateResponse(
        "task_form.html",
        {"request": request, "task": None, "form_title": "Создать новую задачу"}
    )


@app.post("/tasks/new")
async def create_task(
        request: Request,
        title: str = Form(...),
        description: str = Form(None),
        status: str = Form(...),
        priority: str = Form(...),
        deadline: Optional[str] = Form(None),
        db: Session = Depends(get_db)
):
    """Создание новой задачи из формы"""
    from datetime import datetime

    deadline_date = None
    if deadline:
        deadline_date = datetime.fromisoformat(deadline)

    db_task = models.Task(
        title=title,
        description=description,
        status=models.TaskStatus(status),
        priority=models.TaskPriority(priority),
        deadline=deadline_date
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return RedirectResponse(url="/", status_code=303)


@app.get("/tasks/{task_id}/edit")
async def edit_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    """Форма редактирования задачи"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return templates.TemplateResponse(
        "task_form.html",
        {"request": request, "task": task, "form_title": "Редактировать задачу"}
    )


@app.post("/tasks/{task_id}/edit")
async def edit_task(
        request: Request,
        task_id: int,
        title: str = Form(...),
        description: str = Form(None),
        status: str = Form(...),
        priority: str = Form(...),
        deadline: Optional[str] = Form(None),
        db: Session = Depends(get_db)
):
    """Обновление задачи из формы"""
    from datetime import datetime

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = title
    db_task.description = description
    db_task.status = models.TaskStatus(status)
    db_task.priority = models.TaskPriority(priority)

    if deadline:
        db_task.deadline = datetime.fromisoformat(deadline)
    else:
        db_task.deadline = None

    db.commit()
    db.refresh(db_task)

    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Удаление задачи"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()

    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/change-status")
async def change_task_status(
        task_id: int,
        status: str = Form(...),
        db: Session = Depends(get_db)
):
    """Быстрое изменение статуса задачи"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.status = models.TaskStatus(status)
        db.commit()

    return RedirectResponse(url="/", status_code=303)

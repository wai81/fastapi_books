from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_current_user, get_user_exception

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

"""Сеанс работы с базой данных"""


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Класс для расширения основноймодели, проверка валидации на основе pydantic
class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Приоритет долженбыть между 1-5")
    complete: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todos/user/")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()  # производит запись в базу данных

    return successful_response(201)


@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()  # производит запись в базу данных

    return successful_response(200)


@app.delete("/todo_id")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()

    if todo_model is None:
        raise http_exception()

    db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .delete()
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


"""Функция обработки исключения(ошибок)"""


def http_exception():
    return HTTPException(status_code=404, detail="Запись не найдена")

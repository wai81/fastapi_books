from fastapi import FastAPI
""" 
pydantic - модуль python,
позволяющий объявить специальный класс PYTHON,
в котором атрибуты класса имеют статическую типизацию
"""
from pydantic import BaseModel
"""
UUID - библиотека python(универсальный уникальный идентификатор)
"""
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    # создали класс объекта
    id: UUID
    title: str
    author: str
    description: str
    rating: int


BOOKS = []


@app.get("/")
async def read_all_books():
    return BOOKS



from typing import Optional

from fastapi import FastAPI

""" 
pydantic - модуль python,
позволяющий объявить специальный класс PYTHON,
в котором атрибуты класса имеют статическую типизацию
"""
from pydantic import BaseModel, Field

"""
UUID - библиотека python(универсальный уникальный идентификатор)
"""
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    # создали класс объекта
    id: UUID
    title: str = Field(min_length=1)  # Field - неаобходимо для валидации данных
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)  # Optional - означает что параметр не обязателен
    rating: int = Field(gt=-1, lt=101)  # gt-минимальное значение, lt-максимальное значение


BOOKS = []


@app.get("/")
async def read_all_books():
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book

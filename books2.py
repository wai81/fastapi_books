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
    if len(BOOKS) < 1:
        create_books_no_api()
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_books_no_api():
    book1 = BOOKS(id='9318148b-e666-474a-a156-f1c77519bbf1',
                  title='Book 1',
                  author='Author 1',
                  description='Description 1',
                  ratind=50)
    book2 = BOOKS(id='9318149b-e666-474a-a156-f1c77519bbf1',
                  title='Book 2',
                  author='Author 2',
                  description='Description 2',
                  ratind=70)
    book3 = BOOKS(id='9318150b-e666-474a-a156-f1c77519bbf1',
                  title='Book 3',
                  author='Author 3',
                  description='Description 3',
                  ratind=90)
    book4 = BOOKS(id='9318151b-e666-474a-a156-f1c77519bbf1',
                  title='Book 4',
                  author='Author 4',
                  description='Description 4',
                  ratind=80)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)

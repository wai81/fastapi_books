from typing import Optional

from fastapi import FastAPI

""" 
pydantic - модуль python,
позволяющий объявить специальный класс PYTHON,
в котором атрибуты класса имеют статическую типизацию
"""
from pydantic import BaseModel, Field
from uuid import UUID

"""
UUID - библиотека python(универсальный уникальный идентификатор)
"""

app = FastAPI()


class Book(BaseModel):  # создали класс объекта Book
    id: UUID
    title: str = Field(min_length=1)  # Field - неаобходимо для валидации данных
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)  # Optional - означает что параметр не обязателен
    rating: int = Field(gt=-1, lt=101)  # gt-минимальное значение, lt-максимальное значение

    class Config:  # конфигурация класса для документации
        schema_extra = {
            "example": {
                "id": "11f4c2ea-1340-41f4-89f7-2852347bb0d1",
                "title": "Computer Since Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    """
    :param books_to_return: возвращает указанное количестово записей
    """
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_books_no_api():
    book_1 = Book(id="71f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="21f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="31f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="41f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

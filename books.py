from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

"""
GET - запросы
"""
@app.get("/")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My favorite book"}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_title": book_id}

# путь с параметром
@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up" }
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down" }
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Left" }
    return {"Direction": direction_name, "sub": "Right" }

# улучшение параметра пути 
@app.get("/books/{book_name}")
async def read_book_by_name(book_name: str):
    return BOOKS[book_name]

# запросы с параметром
@app.get("/books/")
async def read_all_books_by_parametry(skip_book: Optional[str] = None): # str это не обязательный параметор для запроса 
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

"""
POST - запросы
"""
@app.post("/books/")
async def create_book(booK_title, book_autor):
    curent_book_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > curent_book_id:
                curent_book_id = x
                
    BOOKS[f'book_{curent_book_id + 1}'] = {'title':  booK_title, 'autor': book_autor}
    return BOOKS[f'book_{curent_book_id + 1}']

from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos
from starlette.staticfiles import StaticFiles  # added import base static files

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")  # added 'static' directory in application

app.include_router(auth.router)  # добавляем маршрут auth
app.include_router(todos.router)

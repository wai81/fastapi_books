from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""Подключение к PostgreSQL"""
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost/TodoApplicationsDB"

engine = create_engine(
     SQLALCHEMY_DATABASE_URL
 )

# """Подключение к sqlite"""
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
#
# """Создание подключения к базе"""
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
"""Функция создания сеанса сесии"""
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

""" """
Base = declarative_base()

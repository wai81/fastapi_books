import sys
sys.path.append("..")  # позволяет импортировать все что находится в родительском катологе

from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


SECRET_KEY = "MY_VERY_SECRET_KEY"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",  # добавление прификса для документации
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


# Функция работы с базой данных
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Функция хеширования(шифрования) пароля
def get_password_hash(password):
    return bcrypt_context.hash(password)


# Функция проверки пароля
def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


# Функция авторизации пользователя, проверяем если пользователь в базе и правльный пароль
def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()

    if not user:
        return False  # пользователя не существует
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Фукция создания ключа доступа для пользователя и времени действияключа
def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta]= None):
    encode = {"sub": username,
              "id": user_id}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Фукция чтения ключа доступа и получения имени пользователя и id пользователя
async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username,
                "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not Found")


@router.post("/token")
async def login_for_access_token(response: Response, from_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(from_data.username, from_data.password, db)
    if not user:
        return False  # token_exception()

    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True)

    return True  # {"token": token}


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, from_data=form, db=db)

        if not validate_user_cookie:
            msg = "Не верное 'Имя пользователя' или 'Пароль'"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        ms = "Неизвестная ошибка"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = 'Вы вышли из приложения'
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("register.html", context)


@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...), db: Session = Depends(get_db)):

    validation1 = db.query(models.Users).filter(models.Users.username == username).first()
    validation2 = db.query(models.Users).filter(models.Users.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Неверные данные регистрации"
        context = {"request": request, "msg": msg}
        return templates.TemplateResponse("register.html", context)

    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname
    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = 'Пользователь создан'

    context = {"request": request, "msg": msg}
    return templates.TemplateResponse("login.html", context)

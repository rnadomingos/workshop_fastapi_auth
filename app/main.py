from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core import crud, models, schemas, security
from app.core.config import settings
from app.core.db import engine
from app.core.deps import CurrentUser, SessionDep
from app.core.schemas import Token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def home():
    return {
        "message": "Jornada de Dados"
        }

@app.post("/login/access-token/")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = crud.authenticate(
        db=session, email=form_data.username, password=form_data.password # type: ignore
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

@app.post("/signup", response_model=schemas.User)
async def create_user(session: SessionDep, user: schemas.UserCreate):
    db_user = crud.get_user(db=session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Could not create account")
    return crud.create_user(session, user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: CurrentUser, session: SessionDep):
    db_user = crud.get_user(session, user_id=current_user.id) # type: ignore
    return db_user

@app.get("/users/all/", response_model=list[schemas.User])
async def read_users(current_user: CurrentUser, session: SessionDep):
    db_users = crud.get_users(session)
    return db_users
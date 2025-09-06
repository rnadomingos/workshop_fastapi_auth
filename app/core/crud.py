from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from app.core import models, schemas
from app.core.security import get_password_hash, verify_password

def get_user(
    db: Session,
    user_id: int | None = None,
    email: str | None = None,
):
    if not any([user_id, email]):
        raise ArgumentError("Must provide user_id or email")
    
    query = db.query(models.User)
    if user_id:
        query = query.filter(models.User.id == user_id)
    if email:
        query = query.filter(models.User.email == email)

    return query.first()

def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
        ):
    #return db.query(models.User).offset(skip).limit(limit).all()
    users = db.query(models.User).offset(skip).limit(limit).all()
    print("get_users result:", users)
    return users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email = user.email,
        password = get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, email: str, password: str):
    db_user = get_user(db=db, email=email)
    if not db_user or not verify_password(password, db_user.password):
        return None
    return db_user
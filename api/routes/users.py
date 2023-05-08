from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.routes.endpoints import endpoints
from db import tables, schemas
from db.session import get_db

######################################################
## Router for Users
######################################################

users_router = APIRouter(prefix=endpoints.USERS, tags=["User Operations"])


def get_user(db: Session, user_id: int):
    return db.query(tables.Users).filter(tables.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(tables.Users).filter(tables.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tables.Users).offset(skip).limit(limit).all()


def create_db_user(db: Session, user: schemas.UserCreate):
    db_user = tables.Users(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = tables.Items(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@users_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_db_user(db=db, user=user)


@users_router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return create_user_item(db=db, item=item, user_id=user_id)

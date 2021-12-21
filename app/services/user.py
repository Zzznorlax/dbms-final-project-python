from fastapi import HTTPException
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.database.models import User
from app.schemas import user as schemas


def create_user(db: Session, dto: schemas.UserCreateDTO) -> User:
    user = db.query(User).filter(User.email == dto.email).first()
    if user is not None:
        raise HTTPException(500, "invalid email {}".format(dto.email))

    user = User(dto.name, dto.email, dto.phone, dto.password, dto.kind)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: int, dto: schemas.UserBaseDTO) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(404, "user {} not found".format(user_id))

    user.update(dto.name, dto.phone)

    db.commit()
    db.refresh(user)

    return user


def login(db: Session, dto: schemas.UserLoginDTO) -> Optional[int]:
    user = db.query(User).filter(User.email == dto.email).first()

    if user is None:
        return None

    if not user.verify(dto.email, dto.password):
        return None

    return user.id


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="user {} not found".format(user_id))

    return user


def format_user(user: User) -> Dict:
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'type': user.type,
    }

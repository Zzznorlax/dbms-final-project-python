from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import user as schemas
from app.services import user as service
from app.services import auth as auth_service
from app.utils import auth as auth_utils
from app.utils.config import get_settings, Settings

router = APIRouter()


@router.post("", response_model=schemas.UserRespDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_dto: schemas.UserCreateDTO,
) -> Any:
    """
    Creates new user.
    """

    user = service.create_user(db, user_dto)

    return service.format_user(user)


@router.post("/signIn", response_model=schemas.TokenDTO)
def login(
    *,
    db: Session = Depends(get_db),
    req_dto: schemas.UserLoginDTO,
    config: Settings = Depends(get_settings)
) -> Any:
    """
    Login
    """

    user_id = service.login(db, req_dto)

    if user_id is None:
        raise HTTPException(401, "invalid email or password")

    token = auth_utils.sign_jwt(config.JWT_SECRET, config.JWT_ALGO, user_id, config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        'id': user_id,
        'token': token,
    }


@router.patch("/{id}", response_model=schemas.UserRespDTO)
def update_user(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    req_dto: schemas.UserBaseDTO,
    id: str
) -> Any:
    """
    Updates user.
    """

    user_id = auth_service.verify_jwt(config, token)

    if user_id != int(id):
        raise HTTPException(403, "unauthorized operation")

    user = service.update_user(db, user_id, req_dto)

    return service.format_user(user)


@router.get("/me", response_model=schemas.UserRespDTO)
def get_current_user(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
) -> Any:
    """
    Updates user.
    """

    user_id = auth_service.verify_jwt(config, token)

    user = service.get_user(db, user_id)

    return service.format_user(user)

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import product as schemas
from app.schemas.general import GeneralAPIResp
from app.services import product as service
from app.services import auth as auth_service
from app.utils import auth as auth_utils
from app.utils.config import get_settings, Settings

router = APIRouter()


@router.post("", response_model=schemas.ProductRespDTO, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    product_dto: schemas.ProductCreateDTO,
) -> Any:
    """
    Creates new product.
    """
    user_id = auth_service.verify_jwt(config, token)

    product = service.create_product(db, user_id, product_dto)

    return {
        'data': service.format_product(product)
    }


@router.patch("/{id}", response_model=schemas.ProductRespDTO)
def update_product(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    req_dto: schemas.ProductBaseDTO,
    id: str
) -> Any:
    """
    Updates product.
    """

    user_id = auth_service.verify_jwt(config, token)

    product_id = int(id)

    product = service.get_product(db, product_id)

    if product.owner_id != user_id:
        raise HTTPException(403, "unauthorized operation")

    product = service.update_product(db, product_id, req_dto)

    return {
        'data': service.format_product(product)
    }


@router.get("/{id}", response_model=schemas.ProductRespDTO)
def get_product_by_id(
    *,
    db: Session = Depends(get_db),
    id: str
) -> Any:
    """
    Updates product.
    """

    product_id = int(id)

    product = service.get_product(db, product_id)

    return {
        'data': service.format_product(product)
    }


@router.get("/", response_model=schemas.ProductListRespDTO)
def get_all_products(
    *,
    db: Session = Depends(get_db),
) -> Any:
    """
    Updates product.
    """

    products = service.list_products(db)

    return {
        'data': [service.format_product(product) for product in products]
    }


@router.delete("/{id}", response_model=GeneralAPIResp)
def delete_by_id(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    id: str
) -> Any:
    """
    Updates product.
    """
    user_id = auth_service.verify_jwt(config, token)

    product_id = int(id)

    product = service.get_product(db, product_id)

    if product.owner_id != user_id:
        raise HTTPException(403, "unauthorized operation")

    service.delete_product(db, product_id)

    return {
        'status': 200,
        'message': "product {} deleted".format(id),
    }

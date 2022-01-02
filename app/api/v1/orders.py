from typing import Any, List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import order as schemas
from app.schemas.general import GeneralAPIResp
from app.services import order as service
from app.services import auth as auth_service
from app.utils import auth as auth_utils
from app.utils.config import get_settings, Settings

router = APIRouter()


@router.post("", response_model=schemas.OrderRespDTO, status_code=status.HTTP_201_CREATED)
def create_order(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    req_dto: List[schemas.OrderItemDTO],
) -> Any:
    """
    Creates new order.
    """
    user_id = auth_service.verify_jwt(config, token)

    order = service.create_order(db, user_id, req_dto)

    return {
        'data': service.format_order(order)
    }


@router.patch("/{id}", response_model=schemas.OrderRespDTO)
def update_order(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    req_dto: List[schemas.OrderItemDTO],
    id: str
) -> Any:
    """
    Updates order.
    """

    user_id = auth_service.verify_jwt(config, token)

    order_id = int(id)

    order = service.get_order(db, order_id)

    if order.buyer_id != user_id:
        raise HTTPException(403, "unauthorized operation")

    order = service.update_order(db, order_id, req_dto)

    return {
        'data': service.format_order(order)
    }


@router.get("/{id}", response_model=schemas.OrderRespDTO)
def get_order_by_id(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    id: str
) -> Any:
    """
    Gets order by order ID.
    """

    user_id = auth_service.verify_jwt(config, token)

    order_id = int(id)

    order = service.get_order(db, order_id)

    if user_id != order.buyer_id:
        raise HTTPException(403, "unauthorized operation")

    return {
        'data': service.format_order(order)
    }


@router.get("/", response_model=schemas.OrderListRespDTO)
def get_all_orders(
    *,
    db: Session = Depends(get_db),
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
) -> Any:
    """
    Gets all order.
    """
    user_id = auth_service.verify_jwt(config, token)

    orders = service.list_orders_by_user(db, user_id)

    return {
        'data': [service.format_order(order) for order in orders]
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
    Deletes order.
    """
    user_id = auth_service.verify_jwt(config, token)

    order_id = int(id)

    order = service.get_order(db, order_id)

    if order.buyer_id != user_id:
        raise HTTPException(403, "unauthorized operation")

    service.delete_order(db, order_id)

    return {
        'status': 200,
        'message': "order {} deleted".format(id),
    }

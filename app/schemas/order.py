from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class OrderItemDTO(BaseModel):
    product_id: int = Field(
        ...,
        alias="productId"
    )

    amount: int


class OrderItemRespDTO(OrderItemDTO):
    name: str
    description: str
    picture: str
    price: int


class OrderBaseDTO(BaseModel):

    items: List[OrderItemDTO] = Field(
        ...
    )


class OrderDTO(BaseModel):

    id: int

    buyer_name: str = Field(
        ...,
        alias="buyerName"
    )

    buyer_email: str = Field(
        ...,
        alias="buyerEmail"
    )

    buyer_phone: str = Field(
        ...,
        alias="buyerPhone"
    )

    timestamp: datetime

    products: List[OrderItemRespDTO]


class OrderRespDTO(BaseModel):
    data: OrderDTO


class OrderListRespDTO(BaseModel):
    data: List[OrderDTO]

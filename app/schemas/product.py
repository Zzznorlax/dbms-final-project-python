from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class ProductBaseDTO(BaseModel):

    name: str = Field(
        ...,
        description="Product's name"
    )

    description: str = Field(
        ...
    )

    picture: str = Field(
        ...
    )

    inventory: int = Field(
        ...
    )

    start_sale_time: datetime = Field(
        ...,
        alias="startSaleTime"
    )

    end_sale_time: datetime = Field(
        ...,
        alias="endSaleTime"
    )


class ProductCreateDTO(ProductBaseDTO):

    price: int = Field(
        ...
    )


class ProductDTO(ProductBaseDTO):

    id: int = Field(
        ...,
        description="Product's DB ID"
    )


class ProductRespDTO(BaseModel):
    data: ProductDTO


class ProductListRespDTO(BaseModel):
    data: List[ProductDTO]

from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database.models import Product
from app.schemas import product as schemas


def create_product(db: Session, user_id: int, dto: schemas.ProductCreateDTO) -> Product:

    product = Product(dto.name, dto.description, dto.inventory, dto.price, user_id, dto.start_sale_time, dto.end_sale_time, dto.picture)

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(db: Session, product_id: int, dto: schemas.ProductBaseDTO) -> Product:
    product = db.query(Product).filter(Product.deleted_at.is_(None)).filter(Product.id == product_id).first()  # type: ignore

    if product is None:
        raise HTTPException(404, "product {} not found".format(product_id))

    product.update(dto.name, dto.description, dto.inventory, dto.start_sale_time, dto.end_sale_time, dto.picture)

    db.commit()
    db.refresh(product)

    return product


def get_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.deleted_at.is_(None)).filter(Product.id == product_id).first()  # type: ignore

    if product is None:
        raise HTTPException(status_code=404, detail="product {} not found".format(product_id))

    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.deleted_at.is_(None)).filter(Product.id == product_id).first()  # type: ignore

    if product is None:
        raise HTTPException(status_code=404, detail="product {} not found".format(product_id))

    product.delete()

    db.commit()


def list_products(db: Session) -> List[Product]:
    products = db.query(Product).filter(Product.deleted_at.is_(None))  # type: ignore

    if products is None:
        return []

    return list(products)


def format_product(product: Product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'picture': product.picture,
        'inventory': product.inventory,
        'price': product.price,
        'startSaleTime': product.start_sale_time,
        'endSaleTime': product.end_sale_time,
    }

from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.database.models import Order, OrderItem, User, Product
from app.schemas import order as schemas


def create_order(db: Session, user_id: int, dto: List[schemas.OrderItemDTO]) -> Order:

    order = Order(user_id)

    db.add(order)
    db.flush()
    db.refresh(order)

    for order_dto in dto:
        order_item = OrderItem(order.id, product_id=order_dto.product_id, amount=order_dto.amount)
        db.add(order_item)

    db.commit()
    db.refresh(order)

    order = db.query(Order).join(Order.items).join(OrderItem.product).filter(Order.deleted_at.is_(None)).filter(Order.id == order.id).options(contains_eager(Order.items).contains_eager(OrderItem.product)).first()  # type: ignore

    return order


def update_order(db: Session, order_id: int, dto: List[schemas.OrderItemDTO]) -> Order:
    order = db.query(Order).filter(Order.deleted_at.is_(None)).filter(Order.id == order_id).first()  # type: ignore

    if order is None:
        raise HTTPException(404, "order {} not found".format(order_id))

    order_items = db.query(OrderItem).filter(order_id == order_id)  # type: ignore

    order_item_map = {order_item_dto.product_id: order_item_dto.amount for order_item_dto in dto}

    product_ids = order_item_map.keys()

    for order_item in order_items:
        if order_item.product_id in product_ids:
            order_item.set_delete(False)
            order_item.update(order_item_map[order_item.product_id])
            order_item_map.pop(order_item.product_id)
        else:
            order_item.set_delete(True)

    for product_id, amount in order_item_map.items():
        OrderItem(order_id, product_id, amount)

    db.commit()
    db.refresh(order)

    return order


def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.deleted_at.is_(None)).filter(Order.id == order_id).options(joinedload('*')).first()  # type: ignore

    if order is None:
        raise HTTPException(status_code=404, detail="order {} not found".format(order_id))

    return order


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.deleted_at.is_(None)).filter(Order.id == order_id).first()  # type: ignore

    if order is None:
        raise HTTPException(status_code=404, detail="order {} not found".format(order_id))

    order.delete()

    db.commit()


def list_orders(db: Session) -> List[Order]:
    orders = db.query(Order).filter(Order.deleted_at.is_(None))  # type: ignore

    if orders is None:
        return []

    return list(orders)


def format_order(order: Order):

    buyer: User = order.buyer

    product_dto_list = []
    item: OrderItem
    for item in order.items:
        product: Product = item.product
        product_dto_list.append({
            'productId': product.id,
            'name': product.name,
            'description': product.description,
            'picture': product.picture,
            'price': product.price,
            'amount': item.amount,
        })

    return {
        'id': order.id,
        'timestamp': order.created_at,
        'buyerName': buyer.name,
        'buyerEmail': buyer.email,
        'buyerPhone': buyer.phone,
        'products': product_dto_list,
    }

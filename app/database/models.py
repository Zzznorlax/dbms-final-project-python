
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

from app.schemas.user import UserType
from app.utils.crypto import hash_string, get_random_string


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=False)

    email = Column(String, unique=True, index=True, nullable=False)

    phone = Column(String, nullable=False)

    hashed_password = Column(String, nullable=False)

    salt = Column(String, nullable=False)

    type = Column(Enum(UserType), nullable=False, default=UserType.buyer)

    products = relationship("Product", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, name: str, email: str, phone: str, password: str, type: UserType):
        self.name = name
        self.email = email
        self.type = type
        self.phone = phone

        self.salt = get_random_string(8)

        self.hashed_password = hash_string(email + password + self.salt)

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def verify(self, email: str, password: str) -> bool:
        if self.hashed_password == hash_string(email + password + self.salt):
            return True

        return False

    def update(self, name: str, phone: str):
        self.name = name
        self.phone = phone

        self.updated_at = datetime.now()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=False)

    description = Column(String, nullable=True)

    inventory = Column(Integer)

    price = Column(Integer)

    picture = Column(Integer)

    start_sale_time = Column(DateTime)

    end_sale_time = Column(DateTime)

    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship("User", back_populates="products")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, name: str, description: str, inventory: int, price: int, owner_id: int, start_sale_time: datetime, end_sale_time: datetime, picture: str):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.price = price
        self.owner_id = owner_id
        self.start_sale_time = start_sale_time
        self.end_sale_time = end_sale_time

        self.picture = picture

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, name: str, description: str, inventory: int, start_sale_time: datetime, end_sale_time: datetime, picture: str):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.start_sale_time = start_sale_time
        self.end_sale_time = end_sale_time

        self.picture = picture

        self.updated_at = datetime.now()

    def delete(self):
        self.deleted_at = datetime.now()


class OrderItem(Base):
    __tablename__ = 'order_item'

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship("Product")

    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    order = relationship("Order", back_populates="items")

    amount = Column(Integer)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, order_id: int, product_id: int, amount: int):
        self.order_id = order_id
        self.product_id = product_id
        self.amount = amount

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, amount: int):
        self.amount = amount

        self.updated_at = datetime.now()

    def set_delete(self, delete: bool = True):
        if delete:
            self.deleted_at = datetime.now()
        else:
            self.deleted_at = None


class Order(Base):

    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)

    items = relationship("OrderItem", back_populates="order")

    buyer_id = Column(Integer, ForeignKey('user.id'))
    buyer = relationship("User", back_populates="orders")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, buyer_id: int):
        self.buyer_id = buyer_id

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def delete(self):
        self.deleted_at = datetime.now()

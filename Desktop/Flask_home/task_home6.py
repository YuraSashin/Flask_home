from contextlib import asynccontextmanager
import databases
from fastapi import FastAPI
from sqlalchemy import create_engine, select, insert, update, delete, Column,\
    Integer, String, Text, Boolean, Numeric, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserIn(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

class UserOut(UserIn):
    id: int

class ItemIn(BaseModel):
    title: str
    description: str
    price: Decimal

class ItemOut(ItemIn):
    id: int

class OrderIn(BaseModel):
    user_id: int
    item_id: int
    order_date: date
    delivered: bool = False

class OrderOut(OrderIn):
    id: int

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    orders = relationship('Order', backref='user')

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(scale=2), nullable=False)
    orders = relationship('Order', backref='item')

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    order_date = Column(Date, nullable=False)
    delivered = Column(Boolean, nullable=False, default=False)

DATABASE_URL = 'sqlite:///task_base.sqlite'

db = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan, title='Задание 4', version='1.0')

# получение данных из баз
@app.get('/')
async def index():
    users = await db.fetch_all(select(User))
    users = [UserOut.model_validate({
        'id': user.id,
        'name': user.name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password
        }) for user in users]

    items = await db.fetch_all(select(Item))
    items = [ItemOut.model_validate({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'price': item.price
        }) for item in items]

    orders = await db.fetch_all(select(Order))
    orders = [OrderOut.model_validate({
        'id': order.id,
        'user_id': order.user_id,
        'item_id': order.item_id,
        'order_date': order.order_date,
        'delivered': order.delivered
        }) for order in orders]
    return {'users': users, 'items': items, 'orders': orders}

# CRUD-операции users
@app.get('/users/', response_model=list[UserOut])
async def get_users():
    return await db.fetch_all(select(User))

@app.post('/users/', response_model=UserIn)
async def create_user(user: UserIn):
    new_user = insert(User).values(**user.model_dump())
    await db.execute(new_user)
    return user

@app.get('/users/{user_id}/', response_model=UserOut)
async def get_user(user_id: int):
    return await db.fetch_one(select(User).where(User.id == user_id))

@app.put('/users/{user_id}/', response_model=UserOut)
async def edit_user(user_id: int, new_user: UserIn):
    user_update = (
        update(User)
        .where(User.id == user_id)
        .values(**new_user.model_dump())
    )
    await db.execute(user_update)
    return await db.fetch_one(select(User).where(User.id == user_id))

@app.delete('/users/{user_id}/')
async def delete_user(user_id: int):
    delete_user = delete(User).where(User.id == user_id)
    await db.execute(delete_user)
    return {'deleted': True, 'deleted_user_id': user_id}

# CRUD-операции items
@app.get('/items/', response_model=list[ItemOut])
async def get_items():
    return await db.fetch_all(select(Item))

@app.post('/items/', response_model=ItemIn)
async def create_item(item: ItemIn):
    new_item = insert(Item).values(**item.model_dump())
    await db.execute(new_item)
    return item

@app.get('/items/{item_id}/', response_model=ItemOut)
async def get_item(item_id: int):
    return await db.fetch_one(select(Item).where(Item.id == item_id))

@app.put('/items/{item_id}/', response_model=ItemOut)
async def edit_item(item_id: int, new_item: ItemIn):
    item_update = (
        update(Item)
        .where(Item.id == item_id)
        .values(**new_item.model_dump())
    )
    await db.execute(item_update)
    return await db.fetch_one(select(Item).where(Item.id == item_id))

@app.delete('/items/{item_id}/', response_model=ItemOut)
async def delete_item(item_id: int):
    delete_item = delete(Item).where(Item.id == item_id)
    await db.execute(delete_item)
    return {'deleted': True, 'deleted_item_id': item_id}

# CRUD-операции orders
@app.get('/orders/', response_model=list[OrderOut])
async def get_orders():
    return await db.fetch_all(select(Order))

@app.post('/orders/', response_model=OrderIn)
async def create_order(order: OrderIn):
    new_order = insert(Order).values(**order.model_dump())
    await db.execute(new_order)
    return order

@app.get('/orders/{order_id}/', response_model=OrderOut)
async def get_order(order_id: int):
    return await db.fetch_one(select(Order).where(Order.id == order_id))

@app.put('/orders/{order_id}/', response_model=OrderOut)
async def edit_order(order_id: int, new_order: OrderIn):
    order_update = (
        update(Order)
        .where(Order.id == order_id)
        .values(**new_order.model_dump())
    )
    await db.execute(order_update)
    return await db.fetch_one(select(Order).where(Order.id == order_id))

@app.delete('/orders/{order_id}/', response_model=OrderOut)
async def delete_order(order_id: int):
    delete_order = delete(Order).where(Order.id == order_id)
    await db.execute(delete_order)
    return {'deleted': True, 'deleted_order_id': order_id}
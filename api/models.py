from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Boolean,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Defines the database schema and the models (classes) that represent tables in the database

engine = create_engine(
    "postgresql://dcyjdclp:u1Yz0umjHkXgST5Q-6o3gVTUC79gOx8Y@rogue.db.elephantsql.com/dcyjdclp"
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    price = Column(Float)


class test(Base):
    __tablename__ = "teststock"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    price = Column(Float)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    balance = Column(Float)
    password = Column(String)
    portfolio = relationship("Portfolio", back_populates="user")


class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    shares = Column(Integer)
    user = relationship("User", back_populates="portfolio")
    stock = relationship("Stock")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    type = Column(String)
    price = Column(Float)
    shares = Column(Integer)
    executed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(engine)

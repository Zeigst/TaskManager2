from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, VARCHAR, BOOLEAN
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR, nullable=False)
    password = Column(VARCHAR, nullable=False)
    fullname = Column(VARCHAR, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    todo_list = relationship("TodoList", back_populates="user", cascade="all, delete")

class TodoList(Base):
    __tablename__ = 'todo_lists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(VARCHAR, nullable=False)
    description = Column(VARCHAR)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="todo_list")
    todo_item = relationship("TodoItem", back_populates="todo_list", cascade="all, delete")


class TodoItem(Base):
    __tablename__ = 'todo_items'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('todo_lists.id'), nullable=False)
    name = Column(VARCHAR, nullable=False)
    description = Column(VARCHAR)
    status = Column(BOOLEAN, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    todo_list = relationship("TodoList", back_populates="todo_item")
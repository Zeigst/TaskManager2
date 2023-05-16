from dataclasses import dataclass
from database.models import *
from database.database import *
from sqlalchemy.orm import Session

@dataclass
class CreateTodoItem:
  session: Session
  todo_list: TodoList
  name: str
  description: str
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    new_todo_item = TodoItem(list_id=self.todo_list.id, name=self.name, description=self.description)
    self.session.add(new_todo_item)
    self.session.commit()
    self.success = True
    self.message = "Created new Task"

@dataclass
class EditTodoItemName:
  session: Session
  todo_item: TodoItem
  new_name: str
  old_name: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.old_name = self.todo_item.name
    self.todo_item.name = self.new_name
    self.session.commit()
    self.success = True
    self.message = "Name Updated"

@dataclass
class EditTodoItemDescription:
  session: Session
  todo_item: TodoItem
  new_description: str
  old_description: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.old_description = self.todo_item.description
    self.todo_item.description = self.new_description
    self.session.commit()
    self.success = True
    self.message = "Description Updated"

@dataclass
class ToggleTodoItem:
  session: Session
  todo_item: TodoItem
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.status = not self.todo_item.status
    self.session.commit()
    self.success = True
    self.message = "TodoItem toggled"

@dataclass
class DeleteTodoItem:
  session: Session
  todo_item: TodoItem
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.session.query(TodoItem).filter_by(id=self.todo_item.id).delete()
    self.session.commit()
    self.success = True
    self.message = "TodoItem deleted"


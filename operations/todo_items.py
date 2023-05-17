from dataclasses import dataclass
from database.models import *
from database.database import *
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import make_transient

@dataclass
class CreateTodoItem:
  session: Session
  todo_list: TodoList
  name: str
  description: str
  new_todo_item: TodoItem = None
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.new_todo_item = TodoItem(list_id=self.todo_list.id, name=self.name, description=self.description)
    self.session.add(self.new_todo_item)
    self.session.commit()
    self.success = True
    self.message = "Task Created"

  def undo(self) -> None:
    self.session.query(TodoItem).filter_by(id=self.new_todo_item.id).delete()
    self.session.commit()
    self.message = "Undo Task Creation"

  def redo(self) -> None:
    make_transient(self.new_todo_item)
    self.session.add(self.new_todo_item)
    self.session.commit()
    self.message = "Redo Task Creation"

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

  def undo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.name = self.old_name
    self.session.commit()
    self.message = "Undo Name Change"

  def redo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.name = self.new_name
    self.session.commit()
    self.message = "Redo Name Change"

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

  def undo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.description = self.old_description
    self.session.commit()
    self.message = "Undo Description Change"

  def redo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.description = self.new_description
    self.session.commit()
    self.message = "Redo Description Change"

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

  def undo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.status = not self.todo_item.status
    self.session.commit()
    self.message = "TodoItem toggled"

  def redo(self) -> None:
    self.todo_item = self.session.query(TodoItem).filter_by(id=self.todo_item.id).first()
    self.todo_item.status = not self.todo_item.status
    self.session.commit()
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
    self.message = "Task Deleted"

  def undo(self) -> None:
    make_transient(self.todo_item)
    self.session.add(self.todo_item)
    self.session.commit()
    self.message = "Undo Task Deletion"

  def redo(self) -> None:
    self.session.query(TodoItem).filter_by(id=self.todo_item.id).delete()
    self.session.commit()
    self.message = "Redo Task Deleted"


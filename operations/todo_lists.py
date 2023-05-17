from dataclasses import dataclass, field
from database.models import *
from database.database import *
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import make_transient

@dataclass
class CreateTodoList:
  session: Session
  user: User
  name: str
  description: str
  new_todo_list: TodoList = None
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.new_todo_list = TodoList(user_id=self.user.id, name=self.name, description=self.description)
    self.session.add(self.new_todo_list)
    self.session.commit()
    self.success = True
    self.message = "Task List Created"

  def undo(self) -> None:
    self.session.query(TodoList).filter_by(id=self.new_todo_list.id).delete()
    self.session.commit()
    self.message = "Undo Task List Creation"

  def redo(self) -> None:
    make_transient(self.new_todo_list)
    self.session.add(self.new_todo_list)
    self.session.commit()
    self.message = "Redo Task List Creation"

@dataclass
class EditTodoListName:
  session: Session
  todo_list: TodoList
  new_name: str
  old_name: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.old_name = self.todo_list.name
    self.todo_list.name = self.new_name
    self.session.commit()
    self.success = True
    self.message = "Name Changed"

  def undo(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.todo_list.name = self.old_name
    self.session.commit()
    self.message = "Undo Name Change"

  def redo(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.todo_list.name = self.new_name
    self.session.commit()
    self.message = "Redo Name Change"

@dataclass
class EditTodoListDescription:
  session: Session
  todo_list: TodoList
  new_description: str
  old_description: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.old_description = self.todo_list.description
    self.todo_list.description = self.new_description
    self.session.commit()
    self.success = True
    self.message = "Description Changed"

  def undo(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.todo_list.description = self.old_description
    self.session.commit()
    self.message = "Undo Description Change"

  def redo(self) -> None:
    self.todo_list = self.session.query(TodoList).filter_by(id=self.todo_list.id).first()
    self.todo_list.description = self.new_description
    self.session.commit()
    self.message = "Redo Description Change"

@dataclass
class DeleteTodoList:
  session: Session
  todo_list: TodoList
  todo_items: list[TodoItem] = field(default_factory=list)
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.todo_items = self.session.query(TodoItem).filter_by(list_id=self.todo_list.id).all()
    self.session.query(TodoList).filter_by(id=self.todo_list.id).delete()
    self.session.commit()
    self.success = True
    self.message = "TodoList Deleted"

  def undo(self) -> None:
    for item in self.todo_items:
      make_transient(item)
      self.session.add(item)
    make_transient(self.todo_list)
    self.session.add(self.todo_list)
    self.session.commit()
    self.message = "Undo TodoList Deletion"

  def redo(self) -> None:
    self.session.query(TodoList).filter_by(id=self.todo_list.id).delete()
    self.session.commit()
    self.message = "Redo TodoList Deletion"
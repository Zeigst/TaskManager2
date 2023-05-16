from dataclasses import dataclass
from database.models import *
from database.database import *
from sqlalchemy.orm import Session

@dataclass
class CreateTodoList:
  session: Session
  user: User
  name: str
  description: str
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    new_todo_list = TodoList(user_id=self.user.id, name=self.name, description=self.description)
    self.session.add(new_todo_list)
    self.session.commit()
    self.success = True
    self.message = "Created new Task List"

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
    self.message = "Name Updated"

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
    self.message = "Description Updated"

@dataclass
class DeleteTodoList:
  session: Session
  todo_list: TodoList
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.session.query(TodoList).filter_by(id=self.todo_list.id).delete()
    self.session.commit()
    self.success = True
    self.message = "TodoList deleted"
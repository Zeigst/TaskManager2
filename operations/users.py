from dataclasses import dataclass
from database.models import *
from database.database import *
from sqlalchemy.orm import Session
import re

@dataclass
class CreateNewUser:
  session: Session
  username: str
  fullname: str
  password: str
  confirm_password: str
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    
    regex_username = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
    regex_fullname = '[^a-zA-Z\d\s:]'
    user_existed = self.session.query(User).filter_by(username=self.username).first()
    
    if not re.search(regex_username, self.username):
      self.message = "Invalid Username."  
    elif re.search(regex_fullname, self.fullname):
      self.message = "Invalid Fullname."   
    elif len(self.password) < 6:
      self.message = "Password is too short."
    elif self.password != self.confirm_password:
      self.message = "Password confirmation does not match."
    elif user_existed:
      self.message = "Username already exists."
    else:
      new_user = User(username=self.username, password=self.password, fullname=self.fullname)
      self.session.add(new_user)
      self.session.commit()
      self.success = True
      self.message = "Welcome!"
    
@dataclass
class EditUsername:
  session: Session
  user: User
  new_username: str
  old_username: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    username_existed = self.session.query(User).filter_by(username=self.new_username).first()
    if username_existed:
      self.message = "Username already existed."
    else:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.old_username = self.user.username
      self.user.username = self.new_username
      self.session.commit()
      self.success = True
      self.message = "Username updated."

@dataclass
class EditPassword:
  session: Session
  user: User
  old_password: str
  new_password: str
  confirm_new_password: str
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    if self.old_password != self.user.password:
      self.message = "Incorrect Password"
    elif len(self.new_password) < 6:
      self.message = "Password too short"
    elif self.new_password != self.confirm_new_password:
      self.message = "Password confirmation does not match"
    else:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.password = self.new_password
      self.session.commit()
      self.success = True
      self.message = "Password updated."

@dataclass
class EditFullname:
  session: Session
  user: User
  new_fullname: str
  old_fullname: str = ""
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.user = self.session.query(User).filter_by(id=self.user.id).first()
    self.old_fullname = self.user.fullname
    self.user.fullname = self.new_fullname
    self.session.commit()
    self.success = True
    self.message = "Fullname updated."

@dataclass
class DeleteUser:
  session: Session
  user: User
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    self.session.query(User).filter_by(id=self.user.id).delete()
    self.session.commit()
    self.success = True
    self.message = "User deleted"
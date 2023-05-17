from dataclasses import dataclass
from database.models import *
from database.database import *
from sqlalchemy.orm import Session
from operations.auth import *
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
      new_user = User(username=self.username, password=get_hashed_password(self.password) , fullname=self.fullname)
      self.session.add(new_user)
      self.session.commit()
      self.success = True
      self.message = "Welcome!"

  def undo(self) -> None:
    self.message = "Cannot Undo User Creation."

  def redo(self) -> None:
    self.message = "Cannot Redo User Creation."  

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
      self.message = "Username Change."

  def undo(self) -> None:
    if self.success:  
      username_existed = self.session.query(User).filter_by(username=self.old_username).first()
      if username_existed:
        self.success = False
        self.message = "Username already existed."
      else:
        self.user = self.session.query(User).filter_by(id=self.user.id).first()
        self.user.username = self.old_username
        self.session.commit()
        self.message = "Undo Username Change."

  def redo(self) -> None:
    if self.success:
      username_existed = self.session.query(User).filter_by(username=self.new_username).first()
      if username_existed:
        self.success = False
        self.message = "Username already existed."
      else:
        self.user = self.session.query(User).filter_by(id=self.user.id).first()
        self.user.username = self.new_username
        self.session.commit()
        self.message = "Redo Username Change."

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
    if verify_password(self.old_password, self.user.password):
      self.message = "Incorrect Password"
    elif len(self.new_password) < 6:
      self.message = "Password too short"
    elif self.new_password != self.confirm_new_password:
      self.message = "Password confirmation does not match"
    else:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.password = get_hashed_password(self.new_password)
      self.session.commit()
      self.success = True
      self.message = "Password Change."

  def undo(self) -> None:
    if self.success:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.password = get_hashed_password(self.old_password)
      self.session.commit()
      self.message = "Undo Password Change."

  def redo(self) -> None:
    if self.success:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.password = get_hashed_password(self.new_password)
      self.session.commit()
      self.message = "Redo Password Change."

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
    self.message = "Fullname Changed."

  def undo(self) -> None:
    if self.success:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.fullname = self.old_fullname
      self.session.commit()
      self.message = "Undo Fullname Change."
  
  def redo(self) -> None:
    if self.success:
      self.user = self.session.query(User).filter_by(id=self.user.id).first()
      self.user.fullname = self.new_fullname
      self.session.commit()
      self.message = "Redo Fullname Change."

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
    self.message = "User Deleted"

  def undo(self) -> None:
    self.message = "Cannot Undo User Deletion"

  def redo(self) -> None:
    self.message = "Cannot Redo User Deletion"

@dataclass
class Login:
  session: Session
  input_username: str
  input_password: str
  success: bool = False
  message: str = ""

  def execute(self) -> None:
    user = self.session.query(User).filter_by(username=self.input_username).first()
    if user:
      if not verify_password(self.input_password, user.password):
        self.message = "Incorrect Password"
      else:
        data = {
          "username": f"{user.username}",
          "fullname": f"{user.fullname}",
          "user_id": user.id
        }
        self.success = True
        self.message = create_access_token(data)
    elif user == None:
      self.message = "User Not Found"

  def undo(self) -> None:
    pass

  def redo(self) -> None:
    pass

  def check_success(self) -> bool:
    return self.success
  
  def get_message(self) -> str:
    return self.message
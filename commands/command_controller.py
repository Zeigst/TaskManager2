from dataclasses import dataclass, field
from commands.command_interface import *

@dataclass
class CommandController:
  undo_stack : list[Command] = field(default_factory=list)
  redo_stack : list[Command] = field(default_factory=list)
  last_executed_stack : list[Command] = field(default_factory=list)
  
  def execute(self, command: Command) -> None:
    command.execute()
    self.redo_stack.clear()
    self.undo_stack.append(command)
    self.last_executed_stack.append(command)

  def undo(self) -> None:
    if not self.undo_stack:
      return
    else:
      command: Command = self.undo_stack.pop()
      command.undo()
      self.redo_stack.append(command)
      self.last_executed_stack.append(command)

  def redo(self) -> None:
    if not self.redo_stack:
      return
    else:
      command: Command = self.redo_stack.pop()
      command.redo()
      self.undo_stack.append(command)
      self.last_executed_stack.append(command)

  def check_success(self) -> bool:
    command: Command = self.last_executed_stack.pop()
    self.last_executed_stack.append(command)
    return command.check_success()
  
  def get_message(self) -> str:
    command: Command = self.last_executed_stack.pop()
    self.last_executed_stack.append(command)
    return command.get_message()

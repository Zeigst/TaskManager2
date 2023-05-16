from dataclasses import dataclass
from commands.command_interface import *

@dataclass
class CommandController:
  def execute(self, command: Command) -> None:
    command.execute()
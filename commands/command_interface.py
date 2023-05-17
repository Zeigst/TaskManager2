from typing import Protocol

class Command(Protocol):
  def execute() -> None:
    ...

  def undo() -> None:
    ...

  def redo() -> None:
    ...

  def check_success() -> bool:
    ...

  def get_message() -> str:
    ...
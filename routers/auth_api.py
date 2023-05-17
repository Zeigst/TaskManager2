from fastapi import APIRouter, Depends , HTTPException, status
from database.database import *
from sqlalchemy.orm import Session
from io_models.auth import *

from commands.command_controller import *
from operations.users import *
from operations.todo_lists import *
from operations.todo_items import *
from operations.auth import *

session = create_session()
controller = CommandController()
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login(input: LoginInput, session: Session = Depends(access_database)):
  controller.execute(Login(session, input.username, input.password))
  success = controller.check_success()
  message = controller.get_message()
  if not success:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=message,
      headers={"WWW-Authenticate": "Bearer"},
    )
  return LoginOutput(access_token=message, token_type="bearer")
    
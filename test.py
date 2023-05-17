from commands.command_controller import *
from database.database import *
from operations.users import *
from operations.todo_lists import *
from operations.todo_items import *
from operations.auth import *


session = create_session()
controller = CommandController()

user = session.query(User).filter_by(username="test password").first()

controller.execute(Login(session, "test password", "123456"))
print(controller.check_success())
print(controller.get_message())



# CREATE NEW USER - SUCCESS
# controller.execute(CreateNewUser(session, "test password", "test password", "123456", "123456"))


# EDIT USERNAME - SUCCESS
# controller.execute(EditUsername(session, user, "test2"))

# DELETE USER - SUCCESS
# controller.execute(DeleteUser(session, user))



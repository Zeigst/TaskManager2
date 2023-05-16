from commands.command_controller import *
from database.database import *

session = create_session()
controller = CommandController()

# CREATE NEW USER - SUCCESS
# controller.execute(CreateNewUser(session, "test", "test", "123456", "123456"))

user = session.query(User).filter_by(username="test").first()

# EDIT USERNAME - SUCCESS
# controller.execute(EditUsername(session, user, "test2"))

# DELETE USER - SUCCESS
# controller.execute(DeleteUser(session, user))
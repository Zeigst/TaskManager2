from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import *

def create_database():
    engine = create_engine("postgresql://postgres:CHM19902@localhost/taskmanager")
    Base.metadata.create_all(bind=engine)

def create_session():
    engine = create_engine("postgresql://postgres:CHM19902@localhost/taskmanager")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def access_database():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

create_database()
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/hack.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return ''

class Message(Base):
    __tablename__ = 'messages'
    mess_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message = Column(String(200))

    def __init__(self, user_id, mess):
        self.user_id = user_id
        self.message = mess

    def __str__(self):
        return 'user_id: {} \n message: {}'.format(self.user_id, self.message)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
ss = sessionmaker(bind=engine)
ss.configure(bind=engine)  # Как только у вас появится engine
session = ss()

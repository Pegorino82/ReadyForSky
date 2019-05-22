import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, INTEGER

CBase = declarative_base()

with open('./db_secret.json', 'r') as f:
    secret = json.load(f)

db_settings = {
    "host": "127.0.0.1",
    "db": "keydb"
}
db_settings.update(secret)


class DataBase:

    def __init__(self, db_settings):
        self.engine = create_engine('mysql+mysqlconnector://{username}:{password}@{host}/{db}'.format(**db_settings))
        self.session = self.get_session()
        self.create_base()

    def create_base(self):
        CBase.metadata.create_all(self.engine)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def add(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
            return True
        except Exception as err:
            print('>>>', err)
            self.session.rollback()
            return None

    def get_user(self, username):
        result = self.session.query(Users).filter_by(username=username).first()
        return result


class Users(CBase):
    __tablename__ = 'users'
    user_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    username = Column(VARCHAR(45), nullable=False, unique=True, index=True)
    public_key = Column(LONGTEXT, nullable=True)

    def __init__(self, username, public_key=None):
        self.username = username
        self.public_key = public_key

    def __repr__(self):
        return f'<{self.username}>'

    def __str__(self):
        return f'{self.username} {self.public_key}'


db = DataBase(db_settings)

if __name__ == '__main__':
    pass

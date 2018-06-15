from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
dataset_path = '../../../data/gamma.db'

# engine = create_engine('sqlite:///{}'.format(dataset_path), echo=False)
# Session = sessionmaker(bind=engine)
# session = Session()


class Engine:
    instance = None


class Session:
    instance = None
    maker = None


def get_or_create_engine(path=None):
    if Engine.instance is None:
        Engine.instance = create_engine(
            'sqlite:///{}'.format(path), echo=False)
    return Engine.instance


def get_or_create_session(path=None):
    if Session.instance is None:
        Session.maker = sessionmaker(bind=get_or_create_engine(path))
        Session.instance = Session.maker()
    return Session.instance

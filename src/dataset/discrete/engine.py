from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
dataset_path = '../../../data/gamma.db'
engine = create_engine('sqlite:///{}'.format(dataset_path), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
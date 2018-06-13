from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine(
    'sqlite:////mnt/gluster/hongxwing/Workspace/IncidentEstimation/data/gamma.db',
    echo=False)
Session = sessionmaker(bind=engine)
session = Session()
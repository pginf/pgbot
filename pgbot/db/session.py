import sqlalchemy.orm
from pgbot.db.models import engine

Session = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=True)
session: sqlalchemy.orm.Session = Session()

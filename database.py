
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



connection_url = "postgresql://admin:1234@localhost:5437/missions_db"
engine = create_engine(connection_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


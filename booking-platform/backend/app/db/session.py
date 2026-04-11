from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings 

# create_engine sets up the connection pool to PostgreSQL.
# This is equivalent to configuring the DBContext with UseNpgsql(connectionString).
# pool_pre_ping=True checks if the connection is alive before it uses it - 
# prevents errors after the DB restarts or a connection timed out.

engine = create_engine(settings.DATABASE_URL,pool_pre_ping=True)

# SessionLocal is a factory that creates new database sessions.
# Each call to SessionLocal() gives us one session (= one unit of work).
# autocommit = False -- changes are only saved when we explicitly call db.commit()
# autoflush = False -- SQLAlchemy wouldn't auto sync changes to the DB mid-transaction

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
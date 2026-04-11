from sqlalchemy.orm import declarative_base

# This is the base class that all SQLAlchemy models will inherit from.
# This of this as the equivalent of having all your EF Core entities
# inherit from a common base -- it's what ties them to the ORM System.


#Important : Every time when we create a new model (User,Movie,Show,etc)
# We must import it at the bottom of this file.Alembic reads this file
# to discover all tables when generating migrations. If a model isn't 
# imported here, Alembic wouldn't see it and won't create its table.
Base = declarative_base()

# ---- Import all models below this line ----
# Alembic reads this file to discover tables for migration generation.
# Every new model file we create must be imported here.
from app.models.user import User 
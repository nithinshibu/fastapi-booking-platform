from sqlalchemy.orm import declarative_base

# This is the base class that all SQLAlchemy models will inherit from.
# This of this as the equivalent of having all your EF Core entities
# inherit from a common base -- it's what ties them to the ORM System.


# This file defines Base ONLY - no model imports here.
# Model imports used to live here but caused a cicular import
# Model discovery for Alembic is handled in alembic/env.py instead
Base = declarative_base()


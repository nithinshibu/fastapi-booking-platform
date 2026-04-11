from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

# The repository layer is our Data Access Layer (DAL)
# Its only job is to talk to the Database - no business logic lives here.

# .NET equivalent : a concrete IUserRepository implementation

# Every function takes a 'db: Session' as its first argument.
# The session is injected by the caller (the service) ,not created here.
# This keeps the repository stateless and easy to test.

# We use SQLAlchemy 2.0 style: db.execute(select(...)) instead of the 
# legacy db.query(...) style. Both works, but 2.0 style is the current standard.

def get_by_email(db:Session,email:str) -> User | None:
    """ 
    Fetch a single user by email address. Returns None if not found.

    .NET equivalent : _context.Users.FirstOrDefaultAsync(u=>u.Email == email)

    scalar_one_or_none() returns:
        - The User object if exactly one row matches
        - None if no rows match
        - Raises MultipleResultsFound if somehow more than one matches
        (impossible in our case as email has a unique constraint but good to know)

    """
    statement = select(User).where(User.email == email)
    return db.execute(statement).scalar_one_or_none()

def create(db:Session,email:str,hashed_password:str) -> User:
    """ 
    Insert a new user row and return the fully populated User object.

    .NET equivalent:

            var user = new User {Email = email, HashedPassword = hash};
            _context.Users.Add(user);
            await _context.SaveChangesAsync();
            return user;

    Why db.refresh(user) ?
    After db.commit(), the in-memory 'user' object only has the values we set.
    Server-side defaults (id,created_at,updated_at) were written by PostgreSQL,
    not Python.
    db.refresh() reloads the row from the DB so the returned object has all columns populated - 
    including the auto-generated id.
    
    """
    user = User(email=email,hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
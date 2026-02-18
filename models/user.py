from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __name__ = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str
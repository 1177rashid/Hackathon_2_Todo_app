"""
SQLModel Database Models - Todo App Phase II
Referencing: @specs/database/schema.md

IMPORTANT: User model maps to Better Auth's existing 'user' table.
Do NOT modify Better Auth's schema - only read from it.
"""

from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, Boolean, TIMESTAMP
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """
    User model (managed by Better Auth)

    Table: user (Better Auth's table - READ ONLY)
    Schema: Better Auth uses camelCase columns

    IMPORTANT: This model maps to Better Auth's existing table.
    Do NOT create/modify this table - it's managed by Better Auth.
    """
    __tablename__ = "user"

    # Map to Better Auth's camelCase columns
    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    email: str = Field(sa_column=Column("email", Text, unique=True, index=True))
    emailVerified: bool = Field(sa_column=Column("emailVerified", Boolean, nullable=False))
    name: Optional[str] = Field(sa_column=Column("name", Text, nullable=True))
    image: Optional[str] = Field(sa_column=Column("image", Text, nullable=True))
    createdAt: datetime = Field(sa_column=Column("createdAt", TIMESTAMP, nullable=False))
    updatedAt: datetime = Field(sa_column=Column("updatedAt", TIMESTAMP, nullable=False))

    # Relationship: One user has many tasks
    tasks: list["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Task(SQLModel, table=True):
    """
    Task model

    Table: tasks
    Indexes: user_id, completed, (user_id, completed) composite
    Foreign Key: user_id -> user.id (CASCADE DELETE)
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: Many tasks belong to one user
    user: User = Relationship(back_populates="tasks")

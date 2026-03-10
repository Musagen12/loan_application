from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from typing import Optional

EAT = timezone(timedelta(hours=3))

class Employee(SQLModel, table=True):
	employee_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
	employee_name: str
	employee_phone_number: str = Field(index=True, unique=True)
	password_hash: str

	created_at: datetime = Field(default_factory=lambda: datetime.now(EAT))
	updated_at: Optional[datetime] = Field(
		default_factory=lambda: datetime.now(EAT),
		sa_column_kwargs={"onupdate": lambda: datetime.now(EAT)},
		)
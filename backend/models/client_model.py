from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime, timezone, timedelta, date
from enum import Enum
from typing import Optional, List

EAT = timezone(timedelta(hours=3))

class MaritalStatus(str, Enum):
    married = "married"
    single = "single"
    widowed = "widowed"

class Client(SQLModel, table=True):
    client_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    client_name: str
    national_id_number: str = Field(unique=True, index=True)
    client_phone_number: str = Field(index=True, unique=True)
    client_business_name: str
    client_residence: str
    date_of_birth: date
    next_of_kin_name: str
    next_of_kin_contact: str
    marital_status: MaritalStatus
    number_of_children: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(EAT))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(EAT),
        sa_column_kwargs={"onupdate": lambda: datetime.now(EAT)},
    )

    guarantors: List["Guarantor"] = Relationship(back_populates="client", sa_relationship_kwargs={"cascade": "delete"})   # A client can have multiple guarantors

class Guarantor(SQLModel, table=True):
    guarantor_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    client_id: str = Field(foreign_key="client.client_id")
    guarantor_name: str
    national_id_number: str = Field(unique=True, index=True)
    guarantor_phone_number: str = Field(index=True, unique=True)
    guarantor_business_name: str
    guarantor_business_location: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(EAT))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(EAT),
        sa_column_kwargs={"onupdate": lambda: datetime.now(EAT)},
    )

    client: Client = Relationship(back_populates="guarantors")  # A guarantor can only have one client 
    guarantor_business_photos: List["Guarantor_business_photos"] = Relationship(back_populates="guarantor", sa_relationship_kwargs={"cascade": "delete"})

class Guarantor_business_photos(SQLModel, table=True):
    image_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    guarantor_id: str = Field(foreign_key="guarantor.guarantor_id")
    link: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(EAT))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(EAT),
        sa_column_kwargs={"onupdate": lambda: datetime.now(EAT)},
    )
    guarantor: Guarantor = Relationship(back_populates="guarantor_business_photos")
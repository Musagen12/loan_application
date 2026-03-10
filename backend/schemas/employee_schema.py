from pydantic import BaseModel, field_validator
from datetime import date, datetime
from enum import Enum
from typing import Optional
import re

def normalize_kenyan_phone(v: str) -> str:
    v = v.strip()
    v = re.sub(r"[ \-\(\)]", "", v)

    if v.startswith("+254"):
        v = "0" + v[4:]
    elif v.startswith("254"):
        v = "0" + v[3:]
    elif v.startswith("7"):
        v = "0" + v
    elif v.startswith("01"):
        pass
    elif v.startswith("0"):
        pass
    else:
        raise ValueError(f"Invalid Kenyan phone number prefix: {v}")

    if re.match(r"^07\d{8}$", v):
        return v
    elif re.match(r"^01\d{8}$", v):
        return v
    else:
        raise ValueError(f"Invalid Kenyan phone number format or length: {v}")

class Employee_type(str, Enum):
    admin = "admin"
    regular = "regular"

class Employee_Base(BaseModel):
    employee_name: str
    employee_phone_number:str
    employee_type: Employee_type
    password_hash: str

    @field_validator("employee_phone_number")
    @classmethod
    def validate_phone(cls, v):
        return normalize_kenyan_phone(v)

    class Config:
        from_attributes = True

class Employee(Employee_Base):
    employee_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
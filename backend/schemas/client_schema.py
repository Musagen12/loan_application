from pydantic import BaseModel, field_validator
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
import re


# =========================
# Utility Functions
# =========================

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


def national_id_number_size(v: str) -> str:
    if len(v) != 8:
        raise ValueError("The id number must be exactly 8 digits")
    return v


# =========================
# Enums
# =========================

class MaritalStatus(str, Enum):
    married = "married"
    single = "single"
    widowed = "widowed"


# =========================
# Client Schemas
# =========================

class Client_Base(BaseModel):
    client_name: str
    national_id_number: str
    client_phone_number: str
    client_business_name: str
    client_residence: str
    date_of_birth: date
    next_of_kin_name: str
    next_of_kin_contact: str
    marital_status: MaritalStatus
    number_of_children: int

    @field_validator("client_phone_number", "next_of_kin_contact")
    @classmethod
    def validate_phone(cls, v):
        return normalize_kenyan_phone(v)

    @field_validator("national_id_number")
    @classmethod
    def validate_national_id(cls, v):
        return national_id_number_size(v)

    class Config:
        from_attributes = True


class Client_Lite(BaseModel):
    client_id: str
    client_name: str

    class Config:
        from_attributes = True


# =========================
# Guarantor Schemas
# =========================

class Guarantor_Base(BaseModel):
    client_id: str
    guarantor_name: str
    national_id_number: str
    guarantor_phone_number: str
    guarantor_business_name: str
    guarantor_business_location: str

    @field_validator("guarantor_phone_number")
    @classmethod
    def validate_phone(cls, v):
        return normalize_kenyan_phone(v)

    @field_validator("national_id_number")
    @classmethod
    def validate_national_id(cls, v):
        return national_id_number_size(v)

    class Config:
        from_attributes = True

class Guarantor_Lite(BaseModel):
    guarantor_id: str
    guarantor_name: str


# =========================
# Photo Schemas
# =========================

class GuarantorBusinessPhotoBase(BaseModel):
    guarantor_id: str
    link: str

    class Config:
        from_attributes = True


class GuarantorBusinessPhoto(GuarantorBusinessPhotoBase):
    image_id: str
    created_at: datetime
    updated_at: Optional[datetime]

class GuarantorBusinessPhotoLite(BaseModel):
    image_id: str
    link: str


# =========================
# Full Response Schemas
# =========================

class Guarantor(Guarantor_Base):
    guarantor_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    # client: Optional[Client_Lite]
    guarantor_business_photos: List[GuarantorBusinessPhotoLite] = []

    class Config:
        from_attributes = True

class Client(Client_Base):
    client_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    guarantors: List[Guarantor_Lite] = []

    class Config:
        from_attributes = True
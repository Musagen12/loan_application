from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from core.database import get_session
from sqlmodel import Session, select
from models import client_model
from schemas import client_schema
from typing import List
import os
import uuid
import aiofiles

UPLOAD_DIR = "uploads/guarantors"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024

router = APIRouter(
			prefix="/guarantor", 
			tags=["Guarantor routes"]
		)

# Guarantor routes
@router.get("/", response_model=List[client_schema.Guarantor])
def list_guarantors(session: Session = Depends(get_session)):
    guarantors = session.exec(select(client_model.Guarantor)).all()
    response_guarantors: List[client_schema.Guarantor] = []

    for guarantor in guarantors:
        # Load the business photos for this guarantor
        photos = session.exec(
            select(client_model.Guarantor_business_photos)
            .where(client_model.Guarantor_business_photos.guarantor_id == guarantor.guarantor_id)
        ).all()

        guarantor_business_photos = [
            client_schema.GuarantorBusinessPhotoLite(
                image_id=photo.image_id,
                link=photo.link
            )
            for photo in photos
        ]

        response_guarantors.append(
            client_schema.Guarantor(
                guarantor_id=guarantor.guarantor_id,
                client_id=guarantor.client_id,
                # client=client_schema.Client_Lite(
                #     client_id=guarantor.client.client_id,
                #     client_name=guarantor.client.client_name
                # ) if guarantor.client else None,
                guarantor_name=guarantor.guarantor_name,
                national_id_number=guarantor.national_id_number,
                guarantor_phone_number=guarantor.guarantor_phone_number,
                guarantor_business_name=guarantor.guarantor_business_name,
                guarantor_business_location=guarantor.guarantor_business_location,
                created_at=guarantor.created_at,
                updated_at=guarantor.updated_at,
                guarantor_business_photos=guarantor_business_photos
            )
        )

    return response_guarantors

@router.get("/{guarantor_id}", response_model=client_schema.Guarantor)
def get_guarantor(guarantor_id: str, session: Session = Depends(get_session)):

    statement = (
        select(client_model.Guarantor)
        .where(client_model.Guarantor.guarantor_id == guarantor_id)
        .options(selectinload(client_model.Guarantor.guarantor_business_photos))
    )

    guarantor = session.exec(statement).first()

    if not guarantor:
        raise HTTPException(404, "Guarantor not found")

    return guarantor

@router.post("/", response_model=client_schema.Guarantor)
def create_guarantor(
    guarantor_data: client_schema.Guarantor_Base,
    session: Session = Depends(get_session),
):

    guarantor = client_model.Guarantor(**guarantor_data.model_dump())

    try:
        session.add(guarantor)
        session.commit()
        session.refresh(guarantor)
        return guarantor

    except IntegrityError:
        session.rollback()
        raise HTTPException(400, "Duplicate national ID number")

@router.put("/{guarantor_id}", response_model=client_schema.Guarantor)
def update_client(guarantor_id: str, guarantor_update: client_schema.Guarantor_Base, session: Session = Depends(get_session)):
    guarantor = session.get(client_model.Guarantor, guarantor_id)
    if not guarantor:
        raise HTTPException(status_code=404, detail="Guarantor not found")

    for key, value in guarantor_update.dict().items():
        setattr(guarantor, key, value)

    try:
        session.commit()
        session.refresh(guarantor)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Duplicate national ID number or other constraint violated")

    return guarantor

@router.delete("/{guarantor_id}")
def delete_client(guarantor_id: str, session: Session = Depends(get_session)):
    guarantor = session.get(client_model.Guarantor, guarantor_id)
    if not guarantor:
      raise HTTPException(status_code=404, detail="guarantor not found")

    session.delete(guarantor)
    session.commit()
    return {"message": "Deleted Guarantor"}


# Guarantor business photos routes
@router.post("/{guarantor_id}/photos", response_model=client_schema.Guarantor)
async def upload_photos(
    guarantor_id: str,
    files: List[UploadFile] = File(...),
    session: Session = Depends(get_session),
):
    guarantor = session.get(client_model.Guarantor, guarantor_id)

    if not guarantor:
        raise HTTPException(404, "Guarantor not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:

        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, "Invalid file type")

        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(400, "File too large")

        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        photo = client_model.Guarantor_business_photos(
            guarantor_id=guarantor.guarantor_id,
            link=file_path
        )

        session.add(photo)

    session.commit()
    session.refresh(guarantor)

    return guarantor

@router.delete("/images/{image_id}")
def delete_image(image_id: str, session = Depends(get_session)):
    image = session.get(client_model.Guarantor_business_photos, image_id)

    if not image:
      raise HTTPException(status_code=404, detail="Image not found")

    session.delete(image)
    session.commit()
    return {"message": "Deleted image"}

# If you want to change the guarantor business photo just delete the old one and upload a new one(no need for an update method)
from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from models import client_model
from schemas import client_schema

router = APIRouter(
			prefix="/clients", 
			tags=["Client routes"]
		)

@router.get("/", response_model=list[client_schema.Client])
def get_all_clients(session: Session = Depends(get_session)):
	clients = session.exec(select(client_model.Client)).all()
	return clients

@router.get("/{client_id}", response_model=client_schema.Client)
def get_all_clients(client_id: str, session: Session = Depends(get_session)):
	client = session.get(client_model.Client, client_id)
	return client

@router.post("/", response_model=client_schema.Client)
def create_client(client_data: client_schema.Client_Base, session: Session = Depends(get_session)):
    # Validate next-of-kin
    if client_data.next_of_kin_contact == client_data.client_phone_number:
        raise HTTPException(
            status_code=422,
            detail="The next of kin contact shouldn't be similar to the primary contact"
        )
    
    client = client_model.Client(**client_data.dict())
    try:
        session.add(client)
        session.commit()
        session.refresh(client)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Duplicate national ID number")
    
    return client

@router.put("/{client_id}", response_model=client_schema.Client)
def update_client(client_id: str, client_update: client_schema.Client_Base, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in client_update.dict().items():
        setattr(client, key, value)

    try:
        session.commit()
        session.refresh(client)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Duplicate national ID number or other constraint violated")

    return client

@router.delete("/{client_id}")
def delete_client(client_id: str, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
    	raise HTTPException(status_code=404, detail="Client not found")

    session.delete(client)
    session.commit()
    return {"message": "Deleted client"}
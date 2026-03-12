from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session
from core.security import hash_password
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from models import client_model
from schemas import client_schema
from core.sending_sms import send_sms

router = APIRouter(
    prefix="/clients",
    tags=["Client routes"]
)

# Get all clients
@router.get("/", response_model=list[client_schema.Client])
def get_all_clients(session: Session = Depends(get_session)):
    clients = session.exec(select(client_model.Client)).all()
    return clients

# Get one client based on the client_id
@router.get("/{client_id}", response_model=client_schema.Client)
def get_client(client_id: str, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# Create a client
@router.post("/")
def create_client(client_data: client_schema.Client_Request, session: Session = Depends(get_session)):
    if client_data.next_of_kin_contact == client_data.client_phone_number:
        raise HTTPException(
            status_code=422,
            detail="The next of kin contact shouldn't be similar to the primary contact"
        )

    hashed_pw = hash_password(client_data.password)

    client = client_model.Client(
        client_name=client_data.client_name,
        national_id_number=client_data.national_id_number,
        client_phone_number=client_data.client_phone_number,
        client_business_name=client_data.client_business_name,
        client_residence=client_data.client_residence,
        password_hash=hashed_pw,
        date_of_birth=client_data.date_of_birth,
        next_of_kin_name=client_data.next_of_kin_name,
        next_of_kin_contact=client_data.next_of_kin_contact,
        marital_status=client_data.marital_status,
        number_of_children=client_data.number_of_children
    )

    try:
        session.add(client)
        session.commit()
        session.refresh(client)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Duplicate national ID number")

    # Send SMS to next-of-kin only
    sms_status = {"kin_sms": False}
    try:
        result = send_sms(
            client.next_of_kin_contact,
            f"Hello {client.next_of_kin_name}, {client.client_name}'s account has been created successfully."
        )
        sms_status["kin_sms"] = result.get("status") != "failed"
    except Exception as e:
        print(f"Next-of-kin SMS failed: {str(e)}")

    return {**client.__dict__, "sms_status": sms_status}


# Update password only
@router.patch("/{client_id}/password")
def update_client_password(client_id: str, password_data: client_schema.PasswordUpdate, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.password_hash = hash_password(password_data.password)

    try:
        session.commit()
        session.refresh(client)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update password")

    # Send SMS to client
    sms_status = {"client_sms": False}
    try:
        result = send_sms(
            client.client_phone_number,
            f"Hello {client.client_name}, your password has been updated successfully."
        )
        sms_status["client_sms"] = result.get("status") != "failed"
    except Exception as e:
        print(f"Client SMS failed: {str(e)}")

    return {**client.__dict__, "sms_status": sms_status}


# Update client
@router.put("/{client_id}")
def update_client(client_id: str, client_update: client_schema.Client_Request, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = client_update.dict(exclude_unset=True)

    # Track if next-of-kin contact changed
    next_of_kin_updated = False
    if "next_of_kin_contact" in update_data:
        if update_data["next_of_kin_contact"] != client.next_of_kin_contact:
            next_of_kin_updated = True

    # Handle password separately
    if "password" in update_data:
        hashed_pw = hash_password(update_data.pop("password"))
        client.password_hash = hashed_pw

    # Update other fields
    for key, value in update_data.items():
        setattr(client, key, value)

    try:
        session.commit()
        session.refresh(client)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Duplicate national ID number or other constraint violated"
        )

    # Send SMS to client
    sms_status = {"client_sms": False, "kin_sms": False}
    try:
        result = send_sms(
            client.client_phone_number,
            f"Hello {client.client_name}, your profile has been updated successfully."
        )
        sms_status["client_sms"] = result.get("status") != "failed"
    except Exception as e:
        print(f"Client SMS failed: {str(e)}")

    # Send SMS to next-of-kin if contact updated
    if next_of_kin_updated:
        try:
            result = send_sms(
                client.next_of_kin_contact,
                f"Hello {client.next_of_kin_name}, your contact info has been updated for {client.client_name}'s account as the next of kin."
            )
            sms_status["kin_sms"] = result.get("status") != "failed"
        except Exception as e:
            print(f"Next-of-kin SMS failed: {str(e)}")

    return {**client.__dict__, "sms_status": sms_status}


# Delete client
@router.delete("/{client_id}")
def delete_client(client_id: str, session: Session = Depends(get_session)):
    client = session.get(client_model.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    session.delete(client)
    session.commit()

    # Send SMS to client
    sms_status = {"client_sms": False}
    try:
        result = send_sms(
            client.client_phone_number,
            f"Hello {client.client_name}, your account has been deleted."
        )
        sms_status["client_sms"] = result.get("status") != "failed"
    except Exception as e:
        print(f"Client SMS failed: {str(e)}")

    return {"message": "Deleted client", "sms_status": sms_status}
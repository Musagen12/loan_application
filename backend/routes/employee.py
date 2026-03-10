from fastapi import APIRouter, Depends
from core.database import get_session
from models import employee_model
from schemas import employee_schema
from sqlmodel import Session, select
from core.sending_sms import send_sms
from typing import List

router = APIRouter(
	prefix="/employees",
	tags=["Employee routes"]
	)

@router.get("/", response_model=List[employee_schema.Employee])
def get_employees(session: Session = Depends(get_session)):
	employees = session.exec(select(employee_model.Employee)).all()
	return employees


@router.post("/", response_model=employee_schema.Employee)
def create_employee(employee_data: employee_schema.Employee_Base, session:Session = Depends(get_session)):
    employee = employee_model.Employee(**employee_data.model_dump())

    hashed_pw = hash_password(client_data.password)

    session.add(employee)
    session.commit()
    session.refresh(employee)

    # Prepare SMS message
    sms_status = {"employee_sms": False}
    try:
        message = f"Hello {employee.employee_name}, this is just a confirmation for your registration."
        result = send_sms(employee.employee_phone_number, message)
        sms_status["employee_sms"] = result.get("status") != "failed"
    except Exception as e:
        print(f"employee SMS failed: {str(e)}")

    # Return employee with SMS status
    return {**employee.__dict__, "sms_status": sms_status}
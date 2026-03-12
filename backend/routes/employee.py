from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session
from core.security import hash_password
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
    statement = select(employee_model.Employee).where(
        employee_model.Employee.employee_phone_number == employee_data.employee_phone_number
    )

    phone_number = session.exec(statement).first()
    if phone_number:
        raise HTTPException(status_code=422, detail="Phone number has already been used.")

    hashed_pw = hash_password(employee_data.password_hash)

    employee = employee_model.Employee(
            employee_name=employee_data.employee_name,
            employee_phone_number=employee_data.employee_phone_number,
            employee_type=employee_data.employee_type,
            password_hash=hashed_pw
        )

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


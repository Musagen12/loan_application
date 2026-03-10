from fastapi import APIRouter, Depends
from core import get_session
from models.employee import Employee

router = APIRouter(
	prefix="/employees",
	tags=["Employee routes"]
	)

@router.get
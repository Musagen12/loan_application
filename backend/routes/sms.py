from fastapi import APIRouter, HTTPException, status
from schemas.sms_schema import SMSRequest

router = APIRouter(
        prefix="/sms", 
        tags=["SMS routes"]
    )

@router.post("/send-sms")
def send_sms_endpoint(req: SMSRequest):
    try:
        result = send_sms(req.phone_number, req.message)
        # Mark as success only if status is not "failed"
        success = result.get("status") != "failed"
        return {"success": success, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

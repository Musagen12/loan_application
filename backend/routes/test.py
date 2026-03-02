from fastapi import APIRouter

router = APIRouter(
	tags=["Test Route"]
	)

@router.get("/")
def test_api():
	message = {"Status": "Up and running!!!!!!!!!!!!!!!!!"}
	return message
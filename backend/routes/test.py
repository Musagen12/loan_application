from fastapi import APIRouter

router = APIRouter(
	tags=["Test Route"]
	)

# Just a test route
@router.get("/")
def test_api():
	message = {"Status": "Up and running!!!!!!!!!!!!!!!!!"}
	return message
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import create_db_and_tables
from routes import client, guarantor, test, sms

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Loan management system", lifespan=lifespan)

app.include_router(test.router)
app.include_router(sms.router)
app.include_router(client.router)
app.include_router(guarantor.router)
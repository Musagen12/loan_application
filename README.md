# Loan Application Management API

Backend service for managing **loan clients, guarantors, and SMS notifications**.  
Built with **FastAPI** and **SQLModel**, the system handles borrower registration, guarantor tracking, and automated notifications for important account events.

---

## Features

- Client registration and management
- Guarantor management
- Next-of-kin tracking
- Password hashing for client security
- Automatic SMS notifications
- REST API built with FastAPI
- SQLModel / SQLAlchemy database integration

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI |
| ORM | SQLModel / SQLAlchemy |
| Database | PostgreSQL / SQLite / MySQL |
| HTTP Client | httpx |
| Password Security | Hashing utility |

---

## Project Structure

```
loan_application_backend/
│
├── core/
│   ├── database.py
│   ├── security.py
│   └── sending_sms.py
│
├── models/
│   └── client_model.py
│
├── schemas/
│   ├── client_schema.py
│   └── sms_schema.py
│
├── routers/
│   ├── clients.py
│   └── guarantor.py
│
└── main.py
```

---

## Entities

### Client

Represents a borrower applying for a loan.

| Field | Description |
|-------|-------------|
| Name | Client full name |
| National ID | Unique national identification number |
| Phone Number | Contact phone number |
| Business Name | Name of the client's business |
| Residence | Physical address |
| Date of Birth | Client's date of birth |
| Marital Status | Single / Married / etc. |
| Number of Children | Count of dependents |
| Next-of-Kin Name | Emergency contact name |
| Next-of-Kin Contact | Emergency contact phone number |

> Passwords are **hashed before being stored**.

---

### Guarantor

A guarantor agrees to cover the client's loan if the borrower defaults.

| Field | Description |
|-------|-------------|
| Name | Guarantor full name |
| National ID | Unique national identification number |
| Phone Number | Contact phone number |
| Relationship | Relationship to the client |
| Client ID | Reference to the associated client |

> Guarantors receive SMS notifications when they are added, updated, or removed.

---

## SMS Notification System

The system automatically sends SMS alerts during important events. SMS sending is handled in `core/sending_sms.py`.

### Client Notifications

| Event | Notification |
|-------|-------------|
| Client created | Confirmation SMS |
| Profile updated | Update notification |
| Password updated | Security alert |
| Client deleted | Account deletion notice |

### Next-of-Kin Notifications

Sent **only when a client account is created**.

### Guarantor Notifications

| Event | Notification |
|-------|-------------|
| Guarantor added | Confirmation message |
| Guarantor updated | Profile update notification |
| Guarantor removed | Removal notification |

---

## API Endpoints

### Clients — `/clients`

| Method | Endpoint | Description | SMS Sent To |
|--------|----------|-------------|-------------|
| `GET` | `/clients` | Get all clients | — |
| `GET` | `/clients/{client_id}` | Get client by ID | — |
| `POST` | `/clients` | Create a new client | Client, Next-of-kin |
| `PUT` | `/clients/{client_id}` | Update client profile | Client, Next-of-kin (if contact changes) |
| `PATCH` | `/clients/{client_id}/password` | Update client password | Client |
| `DELETE` | `/clients/{client_id}` | Delete client | Client |

### Guarantors — `/guarantor`

| Method | Endpoint | Description | SMS Sent To |
|--------|----------|-------------|-------------|
| `POST` | `/guarantor` | Add a guarantor | Guarantor |
| `PUT` | `/guarantor/{guarantor_id}` | Update guarantor profile | Guarantor |
| `DELETE` | `/guarantor/{guarantor_id}` | Remove a guarantor | Guarantor |

---

## Getting Started

### Install dependencies

```bash
pip install fastapi uvicorn sqlmodel httpx
```

### Start the server

```bash
uvicorn main:app --reload
```

### API Documentation

Once running, interactive docs are available at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| `400` | Duplicate national ID |
| `404` | Resource not found |
| `422` | Invalid request data |
| `500` | Internal server error |

---

## Future Improvements

- [ ] Authentication and login system
- [ ] Loan issuance module
- [ ] Loan repayment tracking
- [ ] Loan officer / admin roles
- [ ] SMS delivery logs
- [ ] Background task queue for notifications
- [ ] Audit logging for compliance

---

## License

This project is intended for **educational and development purposes**.
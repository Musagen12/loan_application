<div align="center">

# 🏦 Loan Application Management API

**A robust backend service for managing loan clients, guarantors, and SMS notifications.**

Built with **FastAPI** · **SQLModel** · **PostgreSQL**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![SQLModel](https://img.shields.io/badge/SQLModel-ORM-blueviolet?style=flat-square)](https://sqlmodel.tiangolo.com)
[![License](https://img.shields.io/badge/License-Educational-orange?style=flat-square)](#license)

</div>

---

## ✨ Features

- 👤 **Client Registration & Management** — Full borrower lifecycle support
- 🤝 **Guarantor Management** — Track and notify guarantors automatically
- 👨‍👩‍👧 **Next-of-Kin Tracking** — Maintain emergency contact records
- 🔐 **Password Security** — Passwords hashed before storage
- 📱 **Automatic SMS Notifications** — Real-time alerts for all key events
- ⚡ **REST API with FastAPI** — High-performance async endpoints
- 🗄️ **SQLModel / SQLAlchemy ORM** — Flexible database integration

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| ⚡ Framework | FastAPI |
| 🗄️ ORM | SQLModel / SQLAlchemy |
| 💾 Database | PostgreSQL / SQLite / MySQL |
| 🌐 HTTP Client | httpx |
| 🔐 Password Security | Hashing utility |

---

## 📁 Project Structure

```
loan_application_backend/
│
├── 📂 core/
│   ├── database.py        # DB connection & session management
│   ├── security.py        # Password hashing utilities
│   └── sending_sms.py     # SMS notification logic
│
├── 📂 models/
│   └── client_model.py    # SQLModel table definitions
│
├── 📂 schemas/
│   ├── client_schema.py   # Pydantic request/response schemas
│   └── sms_schema.py      # SMS payload schemas
│
├── 📂 routers/
│   ├── clients.py         # Client route handlers
│   └── guarantor.py       # Guarantor route handlers
│
└── main.py                # App entry point
```

---

## 🧩 Entities

### 👤 Client

Represents a borrower applying for a loan.

| Field | Description |
|-------|-------------|
| 📛 Name | Client full name |
| 🪪 National ID | Unique national identification number |
| 📞 Phone Number | Contact phone number |
| 🏪 Business Name | Name of the client's business |
| 🏠 Residence | Physical address |
| 🎂 Date of Birth | Client's date of birth |
| 💍 Marital Status | Single / Married / etc. |
| 👶 Number of Children | Count of dependents |
| 🧑‍🤝‍🧑 Next-of-Kin Name | Emergency contact name |
| 📲 Next-of-Kin Contact | Emergency contact phone number |

> 🔒 Passwords are **hashed before being stored** — plain-text passwords are never persisted.

---

### 🤝 Guarantor

A guarantor agrees to cover the client's loan if the borrower defaults.

| Field | Description |
|-------|-------------|
| 📛 Name | Guarantor full name |
| 🪪 National ID | Unique national identification number |
| 📞 Phone Number | Contact phone number |
| 🔗 Relationship | Relationship to the client |
| 🆔 Client ID | Reference to the associated client |

> 📱 Guarantors receive SMS notifications when they are **added**, **updated**, or **removed**.

---

## 📱 SMS Notification System

Automated SMS alerts are dispatched for all key account events, handled in `core/sending_sms.py`.

### 🧑 Client Notifications

| Event | Notification |
|-------|-------------|
| ✅ Client created | Confirmation SMS |
| ✏️ Profile updated | Update notification |
| 🔑 Password updated | Security alert |
| 🗑️ Client deleted | Account deletion notice |

### 👨‍👩‍👧 Next-of-Kin Notifications

> Sent **only when a client account is created**.

### 🤝 Guarantor Notifications

| Event | Notification |
|-------|-------------|
| ➕ Guarantor added | Confirmation message |
| ✏️ Guarantor updated | Profile update notification |
| ❌ Guarantor removed | Removal notification |

---

## 🔌 API Endpoints

### 👤 Clients — `base: /clients`

| Method | Endpoint | Description | 📱 SMS Sent To |
|--------|----------|-------------|----------------|
| `GET` | `/clients` | Get all clients | — |
| `GET` | `/clients/{client_id}` | Get client by ID | — |
| `POST` | `/clients` | Create a new client | Client + Next-of-kin |
| `PUT` | `/clients/{client_id}` | Update client profile | Client + Next-of-kin* |
| `PATCH` | `/clients/{client_id}/password` | Update password | Client |
| `DELETE` | `/clients/{client_id}` | Delete client | Client |

*\*Next-of-kin notified only if their contact details change.*

### 🤝 Guarantors — `base: /guarantor`

| Method | Endpoint | Description | 📱 SMS Sent To |
|--------|----------|-------------|----------------|
| `POST` | `/guarantor` | Add a guarantor | Guarantor |
| `PUT` | `/guarantor/{guarantor_id}` | Update guarantor | Guarantor |
| `DELETE` | `/guarantor/{guarantor_id}` | Remove a guarantor | Guarantor |

---

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install fastapi uvicorn sqlmodel httpx
```

### 2️⃣ Start the development server

```bash
uvicorn main:app --reload
```

### 3️⃣ Explore the API docs

Once running, open your browser:

| Interface | URL |
|-----------|-----|
| 📘 Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📙 ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## ⚠️ Error Handling

| Status Code | Meaning |
|-------------|---------|
| `400` 🔴 | Duplicate national ID |
| `404` 🟡 | Resource not found |
| `422` 🟠 | Invalid request data |
| `500` 🔴 | Internal server error |

---

## 🔮 Future Improvements

- [ ] 🔐 Authentication and login system
- [ ] 💰 Loan issuance module
- [ ] 📊 Loan repayment tracking
- [ ] 👔 Loan officer / admin roles
- [ ] 📋 SMS delivery logs
- [ ] ⚙️ Background task queue for notifications
- [ ] 📝 Audit logging for compliance

---

## 📄 License

This project is intended for **educational and development purposes**.

---

<div align="center">
  Made with ❤️ using <strong>FastAPI</strong> & <strong>SQLModel</strong>
</div>
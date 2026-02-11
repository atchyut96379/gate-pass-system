from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
from db import get_connection

router = APIRouter()

# =========================
# Pydantic Models
# =========================

class LoginRequest(BaseModel):
    email: str
    password: str


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    flat: str
    role: str


class CreateVisitorRequest(BaseModel):
    visitor_name: str
    visitor_phone: str
    purpose: str
    flat_number: str
    created_by: int


class VerifyOtpRequest(BaseModel):
    flat_number: str
    otp: str
    verified_by: int


# =========================
# LOGIN API
# =========================

@router.post("/login")
def login(data: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Name, Role FROM Users WHERE Email=? AND Password=?",
        (data.email, data.password)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    name, role = user
    return {
        "name": name,
        "role": role
    }


# =========================
# ADMIN – CREATE USER
# =========================

@router.post("/admin/create-user")
def create_user(data: CreateUserRequest):
    if data.role not in ["RESIDENT", "SECURITY"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Users (Name, Email, Password, Phone, FlatNumber, Role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.name,
        data.email,
        data.password,
        data.phone,
        data.flat,
        data.role
    ))

    conn.commit()
    conn.close()

    return {"message": f"{data.role} created successfully"}


# =========================
# RESIDENT – CREATE VISITOR
# =========================

@router.post("/resident/create-visitor")
def create_visitor(data: CreateVisitorRequest):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.now() + timedelta(minutes=5)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Visitors
        (VisitorName, VisitorPhone, Purpose, FlatNumber, OTP, OTPExpiry, Status, CreatedBy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.visitor_name,
        data.visitor_phone,
        data.purpose,
        data.flat_number,
        otp,
        expiry,
        "CREATED",
        data.created_by
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Visitor pass created",
        "otp": otp,
        "valid_till": expiry
    }


# =========================
# SECURITY – VERIFY OTP
# =========================

@router.post("/security/verify-otp")
def verify_otp(data: VerifyOtpRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT VisitorId, OTPExpiry, Status
        FROM Visitors
        WHERE FlatNumber=? AND OTP=?
    """, (data.flat_number, data.otp))

    visitor = cursor.fetchone()

    if not visitor:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid OTP or Flat Number")

    visitor_id, expiry, status = visitor

    if status != "CREATED":
        conn.close()
        raise HTTPException(status_code=400, detail="OTP already used or invalid")

    if datetime.now() > expiry:
        cursor.execute(
            "UPDATE Visitors SET Status='EXPIRED' WHERE VisitorId=?",
            visitor_id
        )
        conn.commit()
        conn.close()
        raise HTTPException(status_code=400, detail="OTP expired")

    # APPROVE ENTRY
    cursor.execute(
        "UPDATE Visitors SET Status='APPROVED' WHERE VisitorId=?",
        visitor_id
    )

    cursor.execute("""
        INSERT INTO EntryLogs (VisitorId, VerifiedBy, Status)
        VALUES (?, ?, ?)
    """, (visitor_id, data.verified_by, "APPROVED"))

    conn.commit()
    conn.close()

    return {"message": "Visitor entry approved"}

@router.get("/admin-security/visitor-history")
def all_visitor_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            VisitorName,
            VisitorPhone,
            Purpose,
            FlatNumber,
            Status,
            CreatedAt
        FROM Visitors
        ORDER BY CreatedAt DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "visitor_name": row[0],
            "visitor_phone": row[1],
            "purpose": row[2],
            "flat_number": row[3],
            "status": row[4],
            "created_at": row[5]
        })

    return history
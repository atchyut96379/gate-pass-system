from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
from .db import get_connection

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
        "SELECT name, role FROM users WHERE email=%s AND password=%s",
        (data.email, data.password)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "name": user[0],
        "role": user[1]
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
        INSERT INTO users (name, email, password, phone, flatnumber, role)
        VALUES (%s, %s, %s, %s, %s, %s)
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
        INSERT INTO visitors
        (visitorname, visitorphone, purpose, flatnumber, otp, otpexpiry, status, createdby)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        SELECT visitorid, otpexpiry, status
        FROM visitors
        WHERE flatnumber=%s AND otp=%s
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
            "UPDATE visitors SET status='EXPIRED' WHERE visitorid=%s",
            (visitor_id,)
        )
        conn.commit()
        conn.close()
        raise HTTPException(status_code=400, detail="OTP expired")

    # APPROVE ENTRY
    cursor.execute(
        "UPDATE visitors SET status='APPROVED' WHERE visitorid=%s",
        (visitor_id,)
    )

    cursor.execute("""
        INSERT INTO entrylogs (visitorid, verifiedby, status)
        VALUES (%s, %s, %s)
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
            visitorname,
            visitorphone,
            purpose,
            flatnumber,
            status,
            createdat
        FROM visitors
        ORDER BY createdat DESC
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

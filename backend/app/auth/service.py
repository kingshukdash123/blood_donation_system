from fastapi import HTTPException, Response, Cookie
from app.auth.access_token import (
    hash_password, verify_password,
    create_access_token, decode_access_token
)
from app.db.query.auth import *


def signup_user(user):
    if is_exist_user(user.phone):
        raise HTTPException(400, "User already exists")

    user.password = hash_password(user.password[:72])
    user_id = create_user_query(user)

    if user.role == "hospital":
        create_hospital_profile(user_id, user)

    elif user.role == "blood_bank":
        create_blood_bank_profile(user_id, user)

    elif user.role == "donor":
        create_donor_profile(user_id, user)

    return {
        "message": "Registration successful. Await admin verification.",
        "user_id": user_id
    }


def login_user(user, response: Response):
    db_user = is_exist_user(user.phone)

    if not db_user or not verify_password(user.password, db_user["password_hash"]) or db_user['role'] != user.role:
        raise HTTPException(401, "Invalid credentials")

    if not db_user["is_verified"]:
        raise HTTPException(403, "User not verified")

    token = create_access_token({"sub": db_user["phone"]})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {
        "message": "Login successful",
        "role": db_user["role"]
    }


def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(401, "Not authenticated")

    payload = decode_access_token(access_token)
    if not payload:
        raise HTTPException(401, "Invalid token")

    user = fetch_user_by_phone(payload["sub"])
    if not user:
        raise HTTPException(401, "User not found")

    return user

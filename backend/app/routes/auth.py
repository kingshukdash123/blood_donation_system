from fastapi import APIRouter, Depends, Response
from app.schema.auth import (
    CreateHospitalUser,
    CreateBloodBankUser,
    CreateDonorUser, 
    UserLogIn
)
from app.auth.service import signup_user, login_user, get_current_user

route = APIRouter(prefix="/auth", tags=["Authentication"])


@route.post("/register")
def register_user(
    user: CreateDonorUser
    | CreateBloodBankUser
    | CreateHospitalUser
):
    return signup_user(user)


@route.post("/login")
def login(user: UserLogIn, response: Response):
    return login_user(user, response)


@route.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@route.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "name": user["name"],
        "phone": user["phone"],
        "role": user["role"],
        "verified": user["is_verified"]
    }

"""
ExamHub - Authentication Endpoints
Login, Current User profile, Password change, Logout
"""

from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth.schemas import LoginRequest, TokenResponse, UserProfileDTO, PasswordChangeRequest, TokenData
from backend.app.auth.service import AuthService
from backend.app.auth.dependencies import get_current_user_data
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.core.exceptions import ExamHubException

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    try:
        profile, token = AuthService.authenticate_user(request.username_or_email, request.password)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=profile
        )
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.get("/me", response_model=UserProfileDTO)
def get_me(user: TokenData = Depends(get_current_user_data)):
    try:
        return AuthService.get_user_profile(user.sub)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.post("/change-password")
def change_password(request: PasswordChangeRequest, user: TokenData = Depends(get_current_user_data)):
    try:
        AuthService.change_password(user.sub, request.current_password, request.new_password)
        return {"message": "Password updated successfully."}
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.post("/logout")
def logout(user: TokenData = Depends(get_current_user_data)):
    return {"message": "Logged out successfully."}

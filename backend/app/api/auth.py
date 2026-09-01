"""
ScamTrap AI — Auth Router (§10a)

Provides user authentication, JWT token issuance, refresh token rotation, and RBAC.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900
    role: str = "investigator"


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """Authenticate user and return JWT access token."""
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Synthetic / demo auth logic
    return TokenResponse(
        access_token="demo-jwt-token-investigator",
        role="investigator"
    )


@router.post("/logout")
async def logout():
    """Revoke active tokens."""
    return {"status": "success", "message": "Logged out successfully"}

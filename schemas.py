# schemas.py - Pydantic schemas for request/response validation

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ─────────────────────────────────────────────
# Auth Schemas
# ─────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
    full_name: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ─────────────────────────────────────────────
# User Schemas
# ─────────────────────────────────────────────
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "student"
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    phone: Optional[str]
    profile_picture: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None


# ─────────────────────────────────────────────
# Tutor Schemas
# ─────────────────────────────────────────────
class TutorProfileCreate(BaseModel):
    bio: Optional[str] = None
    subjects: str
    education: Optional[str] = None
    experience_years: int = 0
    hourly_rate: float = Field(..., gt=0)
    location: str
    teaching_mode: str = "Both"
    languages: str = "English"


class TutorProfileUpdate(BaseModel):
    bio: Optional[str] = None
    subjects: Optional[str] = None
    education: Optional[str] = None
    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = None
    location: Optional[str] = None
    teaching_mode: Optional[str] = None
    is_available: Optional[bool] = None
    languages: Optional[str] = None


class TutorResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    subjects: str
    education: Optional[str]
    experience_years: int
    hourly_rate: float
    location: str
    teaching_mode: str
    is_verified: bool
    is_available: bool
    rating: float
    total_reviews: int
    total_students: int
    languages: str
    created_at: datetime
    # Nested user info
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Booking Schemas
# ─────────────────────────────────────────────
class BookingCreate(BaseModel):
    tutor_id: int
    subject: str
    session_date: str
    session_time: str
    duration_hours: float = 1.0
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    student_id: int
    tutor_id: int
    subject: str
    session_date: str
    session_time: str
    duration_hours: float
    total_price: float
    status: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class BookingUpdate(BaseModel):
    status: str


# ─────────────────────────────────────────────
# Review Schemas
# ─────────────────────────────────────────────
class ReviewCreate(BaseModel):
    tutor_id: int
    booking_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    student_id: int
    tutor_id: int
    booking_id: Optional[int]
    rating: int
    comment: Optional[str]
    created_at: datetime
    student: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Search Schema
# ─────────────────────────────────────────────
class TutorSearchParams(BaseModel):
    subject: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    teaching_mode: Optional[str] = None
    sort_by: Optional[str] = "rating"  # rating, price_asc, price_desc

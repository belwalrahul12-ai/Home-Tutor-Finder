# models.py - SQLAlchemy ORM models (Database Table Definitions)

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class UserRole(str, enum.Enum):
    student = "student"
    tutor = "tutor"
    admin = "admin"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


# ─────────────────────────────────────────────
# Users Table - stores all users (students, tutors, admins)
# ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.student)
    phone = Column(String(20), nullable=True)
    profile_picture = Column(String(255), nullable=True, default="/images/default-avatar.png")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tutor_profile = relationship("TutorProfile", back_populates="user", uselist=False)
    bookings_as_student = relationship("Booking", foreign_keys="Booking.student_id", back_populates="student")
    reviews_given = relationship("Review", foreign_keys="Review.student_id", back_populates="student")


# ─────────────────────────────────────────────
# Tutors Table - extended profile for tutor users
# ─────────────────────────────────────────────
class TutorProfile(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    subjects = Column(String(500), nullable=False)         # Comma-separated: "Math,Physics,Chemistry"
    education = Column(String(255), nullable=True)
    experience_years = Column(Integer, default=0)
    hourly_rate = Column(Float, nullable=False)
    location = Column(String(150), nullable=False)
    teaching_mode = Column(String(50), default="Both")     # Online, In-Person, Both
    is_verified = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    total_students = Column(Integer, default=0)
    languages = Column(String(200), default="English")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="tutor_profile")
    bookings = relationship("Booking", foreign_keys="Booking.tutor_id", back_populates="tutor")
    reviews = relationship("Review", foreign_keys="Review.tutor_id", back_populates="tutor")


# ─────────────────────────────────────────────
# Bookings Table - student-tutor session bookings
# ─────────────────────────────────────────────
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutors.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    session_date = Column(String(50), nullable=False)     # ISO date string
    session_time = Column(String(50), nullable=False)
    duration_hours = Column(Float, default=1.0)
    total_price = Column(Float, nullable=False)
    status = Column(String(30), default=BookingStatus.pending)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("User", foreign_keys=[student_id], back_populates="bookings_as_student")
    tutor = relationship("TutorProfile", foreign_keys=[tutor_id], back_populates="bookings")


# ─────────────────────────────────────────────
# Reviews Table - student reviews for tutors
# ─────────────────────────────────────────────
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutors.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    rating = Column(Integer, nullable=False)              # 1-5 stars
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("User", foreign_keys=[student_id], back_populates="reviews_given")
    tutor = relationship("TutorProfile", foreign_keys=[tutor_id], back_populates="reviews")

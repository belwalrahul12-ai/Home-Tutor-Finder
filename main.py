# main.py - FastAPI Application Entry Point

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from database import engine, get_db, Base
import models
from auth import hash_password
from routes import users, tutors, bookings

# ─── Create all database tables ───────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ─── Initialize FastAPI app ───────────────────────────────────────────────────
app = FastAPI(
    title="Home Tutor Finder API",
    description="REST API for connecting students with private tutors",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ─── CORS Middleware ──────────────────────────────────────────────────────────
# Allow frontend (running on any port during development) to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routers ─────────────────────────────────────────────────────────
app.include_router(users.router)
app.include_router(tutors.router)
app.include_router(bookings.router)


# ─── Root Endpoint ────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Welcome to Home Tutor Finder API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Home Tutor Finder API"}


# ─── Seed Sample Data ─────────────────────────────────────────────────────────
def seed_data():
    """Populate database with realistic sample data for demo purposes"""
    db: Session = next(get_db())

    # Skip if data already exists
    if db.query(models.User).count() > 0:
        db.close()
        return

    print("🌱 Seeding sample data...")

    # --- Create Admin ---
    admin = models.User(
        full_name="Admin User",
        email="admin@tutorfinder.com",
        hashed_password=hash_password("Admin@123"),
        role="admin",
        phone="+91-9000000000",
    )
    db.add(admin)

    # --- Create Sample Students ---
    students_data = [
        {"full_name": "Arjun Sharma", "email": "arjun@student.com", "phone": "+91-9111111111"},
        {"full_name": "Priya Patel", "email": "priya@student.com", "phone": "+91-9222222222"},
        {"full_name": "Rohit Mehta", "email": "rohit@student.com", "phone": "+91-9333333333"},
    ]
    students = []
    for s in students_data:
        user = models.User(
            full_name=s["full_name"],
            email=s["email"],
            hashed_password=hash_password("Student@123"),
            role="student",
            phone=s["phone"],
        )
        db.add(user)
        students.append(user)

    # --- Create Sample Tutors ---
    tutors_data = [
        {
            "full_name": "Dr. Kavya Reddy",
            "email": "kavya@tutor.com",
            "phone": "+91-9444444444",
            "bio": "PhD in Mathematics from IIT Delhi. 8+ years of teaching experience. Specialized in Calculus, Algebra, and Statistics. Passionate about making math approachable for every student.",
            "subjects": "Mathematics,Calculus,Algebra,Statistics",
            "education": "PhD Mathematics, IIT Delhi",
            "experience_years": 8,
            "hourly_rate": 800.0,
            "location": "Delhi, India",
            "teaching_mode": "Both",
            "languages": "English,Hindi",
        },
        {
            "full_name": "Mr. Rahul Singh",
            "email": "rahul@tutor.com",
            "phone": "+91-9555555555",
            "bio": "Former software engineer at Google, now a full-time coding tutor. Expert in Python, Data Structures, Web Development, and Machine Learning fundamentals.",
            "subjects": "Python,Data Structures,Web Development,Machine Learning",
            "education": "B.Tech Computer Science, NIT Trichy",
            "experience_years": 5,
            "hourly_rate": 1200.0,
            "location": "Bangalore, India",
            "teaching_mode": "Online",
            "languages": "English,Tamil,Hindi",
        },
        {
            "full_name": "Ms. Ananya Iyer",
            "email": "ananya@tutor.com",
            "phone": "+91-9666666666",
            "bio": "IELTS and TOEFL certified English teacher with a passion for communication skills, creative writing, and grammar. Helped 200+ students achieve band 8+.",
            "subjects": "English,Grammar,Creative Writing,IELTS Prep",
            "education": "MA English Literature, Mumbai University",
            "experience_years": 6,
            "hourly_rate": 600.0,
            "location": "Mumbai, India",
            "teaching_mode": "Both",
            "languages": "English,Hindi,Marathi",
        },
        {
            "full_name": "Prof. Suresh Kumar",
            "email": "suresh@tutor.com",
            "phone": "+91-9777777777",
            "bio": "Retired physics professor with 20 years of academic experience. Specializes in JEE and NEET preparation. Known for simplifying complex concepts.",
            "subjects": "Physics,Chemistry,JEE Preparation,NEET Preparation",
            "education": "M.Sc Physics, Pune University",
            "experience_years": 20,
            "hourly_rate": 1500.0,
            "location": "Pune, India",
            "teaching_mode": "In-Person",
            "languages": "English,Hindi,Marathi",
        },
        {
            "full_name": "Ms. Deepa Nair",
            "email": "deepa@tutor.com",
            "phone": "+91-9888888888",
            "bio": "CA and finance tutor specializing in Accountancy, Economics and Business Studies. Perfect for Class 11-12 Commerce students and CA Foundation aspirants.",
            "subjects": "Accountancy,Economics,Business Studies,CA Foundation",
            "education": "CA, ICAI & B.Com (Hons), Delhi University",
            "experience_years": 4,
            "hourly_rate": 900.0,
            "location": "Chennai, India",
            "teaching_mode": "Online",
            "languages": "English,Malayalam,Tamil",
        },
    ]

    db.flush()  # Flush to get admin ID

    tutor_users = []
    for t in tutors_data:
        user = models.User(
            full_name=t["full_name"],
            email=t["email"],
            hashed_password=hash_password("Tutor@123"),
            role="tutor",
            phone=t["phone"],
        )
        db.add(user)
        tutor_users.append((user, t))

    db.flush()  # Get user IDs

    # Flush students to get IDs
    for s in students:
        db.flush()

    # Create tutor profiles with pre-seeded ratings
    ratings = [4.8, 4.9, 4.7, 4.6, 4.5]
    reviews_count = [47, 63, 38, 92, 29]
    tutor_profiles = []

    for i, (user, data) in enumerate(tutor_users):
        profile = models.TutorProfile(
            user_id=user.id,
            bio=data["bio"],
            subjects=data["subjects"],
            education=data["education"],
            experience_years=data["experience_years"],
            hourly_rate=data["hourly_rate"],
            location=data["location"],
            teaching_mode=data["teaching_mode"],
            languages=data["languages"],
            is_verified=True,
            rating=ratings[i],
            total_reviews=reviews_count[i],
            total_students=reviews_count[i] + 10,
        )
        db.add(profile)
        tutor_profiles.append(profile)

    db.flush()

    # --- Create Sample Reviews ---
    sample_reviews = [
        {"rating": 5, "comment": "Dr. Kavya is absolutely brilliant! She made calculus seem easy. Highly recommend!"},
        {"rating": 5, "comment": "Rahul's coding sessions are gold. I landed my first internship thanks to him!"},
        {"rating": 4, "comment": "Ananya helped me crack IELTS with Band 8. Great teacher, very patient."},
        {"rating": 5, "comment": "Prof. Suresh has a unique way of explaining Physics. My JEE score improved significantly."},
        {"rating": 4, "comment": "Deepa ma'am's Accountancy classes are structured and thorough. Worth every rupee."},
    ]

    db.flush()
    for i, student in enumerate(students[:min(len(students), len(tutor_profiles))]):
        review = models.Review(
            student_id=student.id,
            tutor_id=tutor_profiles[i % len(tutor_profiles)].id,
            rating=sample_reviews[i]["rating"],
            comment=sample_reviews[i]["comment"],
        )
        db.add(review)

    db.commit()
    print("✅ Sample data seeded successfully!")
    print("\n📋 Sample Login Credentials:")
    print("  Admin:   admin@tutorfinder.com   / Admin@123")
    print("  Student: arjun@student.com       / Student@123")
    print("  Tutor:   kavya@tutor.com         / Tutor@123")
    db.close()


# ─── Run seed on startup ──────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    seed_data()


# ─── Run server directly ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

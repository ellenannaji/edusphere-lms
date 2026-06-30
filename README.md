📚 EduSphere – Full Stack Learning Management System (LMS)

EduSphere is a full-stack, web-based Learning Management System designed for structured online learning.
It enables students to register, access courses, watch video lectures, attempt quizzes, track performance, and download certificates.

The system is built using Flask and SQLite, focusing on simplicity, scalability, and real-world LMS workflow design.

📖 Table of Contents
Project Motivation
Key Features
Tech Stack
System Architecture
Database Schema
Quiz & Scoring System
Certificate Generation
Project Structure
Installation & Setup
Future Enhancements
🎯 Project Motivation

Modern learning platforms often require multiple tools for:

Course delivery
Assessment
Progress tracking

EduSphere solves this by providing a single unified LMS system where:

Students can learn and test knowledge in one place
Administrators can manage courses easily
Learning progress is tracked automatically

This project demonstrates full-stack development skills including backend logic, database design, and UI integration.

✨ Key Features
👤 Authentication System
Secure user registration and login
Session-based access control
📚 Course Management
Multiple courses supported
Course descriptions and instructor info
🎥 Video Learning Module
Embedded YouTube video integration
Structured course lessons
📝 Quiz System
MCQ-based evaluation
Auto scoring system
Instant result generation
📊 Progress Tracking
Score calculation
Percentage performance tracking
Stored history per user
🎓 Certificate Generator
Generates PDF certificates for students scoring above threshold
Personalized certificate with name and score
🛠️ Tech Stack
Layer	Technology
Frontend	HTML5, CSS3
Backend	Python Flask
Database	SQLite
Tools	VS Code, Git, GitHub
🧠 System Architecture

EduSphere follows a simple MVC-style structure:

Frontend: HTML templates rendered using Flask
Backend: Flask routes handle logic and APIs
Database: SQLite stores users, courses, quizzes, and results

Flow:

User → Flask Routes → SQLite DB → Template Rendering → Response
🗄️ Database Schema
Users
id
name
email
password
Courses
id
name
description
instructor
Videos
id
course_id
title
video_url
Quizzes
id
course_id
question
options (A–D)
correct_answer
Quiz Results
id
user_id
course_id
score
total
percentage
📝 Quiz & Scoring System
Each quiz question is stored in database
Student responses are evaluated in backend
Score is calculated in real time
Percentage is computed as:
percentage = (score / total) × 100
Results are stored in quiz_results table
🎓 Certificate Generation
Uses ReportLab (PDF library)
Certificate generated when:
Student score ≥ 70%
Includes:
Student name
Course completion status
Score & percentage
📁 Project Structure
Online-Learning-Platform/
│
├── app.py
├── users.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── courses.html
│   ├── course_details.html
│   ├── quiz.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── (assets)
│
├── videos/
├── notes/
└── README.md
🚀 Installation & Setup
1. Clone Repository
git clone https://github.com/ellenannaji/edusphere-lms.git
cd edusphere-lms
2. Install Dependencies
pip install flask reportlab
3. Run Project
python app.py

Open:

http://127.0.0.1:5000
📈 Future Enhancements
Leaderboard system 🏆
Payment gateway integration 💳
AI-based course recommendations 🤖
Mobile responsive UI 📱
Cloud deployment (Render / AWS) 🌐
👨‍💻 Author

Developed by: Ellen Ann Aji
Role: CSE Student | Full Stack Developer


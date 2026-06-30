from flask import Flask, render_template, request, redirect, send_from_directory, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"


# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        instructor TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        title TEXT,
        video_url TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_id INTEGER,
        score INTEGER,
        total INTEGER,
        percentage REAL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- INIT DATA ----------------

def add_courses():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")
    if not cursor.fetchall():
        cursor.executemany("""
        INSERT INTO courses(name,description,instructor)
        VALUES (?,?,?)
        """, [
            ("Python Programming", "Learn Python from basics to advanced concepts", "EduSphere Team"),
            ("Web Development", "Learn HTML, CSS and JavaScript", "EduSphere Team"),
            ("Machine Learning", "Learn AI and ML concepts", "EduSphere Team")
        ])

    conn.commit()
    conn.close()


def add_videos():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM videos")
    if not cursor.fetchall():
        cursor.executemany("""
        INSERT INTO videos(course_id,title,video_url)
        VALUES (?,?,?)
        """, [
            (1, "Python Introduction", "https://www.youtube.com/embed/rfscVS0vtbw"),
            (2, "HTML CSS JavaScript Basics", "https://www.youtube.com/embed/G3e-cpL7ofc"),
            (3, "Machine Learning Introduction", "https://www.youtube.com/embed/Gv9_4yMHFhI")
        ])

    conn.commit()
    conn.close()


def add_quiz():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes")
    if not cursor.fetchall():
        cursor.executemany("""
        INSERT INTO quizzes(course_id,question,option_a,option_b,option_c,option_d,correct_answer)
        VALUES (?,?,?,?,?,?,?)
        """, [
            (1, "Which language is used for web styling?", "HTML", "CSS", "Python", "Java", "B"),
            (1, "Which is a Python framework?", "Django", "Laravel", "React", "Spring", "A")
        ])

    conn.commit()
    conn.close()


create_database()
add_courses()
add_videos()
add_quiz()


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users(name,email,password)
            VALUES (?,?,?)
            """, (
                request.form["name"],
                request.form["email"],
                request.form["password"]
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users WHERE email=? AND password=?
        """, (request.form["email"], request.form["password"]))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


# ---------------- COURSES ----------------

@app.route("/courses")
def courses():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)


# ---------------- COURSE DETAILS ----------------

@app.route("/course/<int:id>")
def course_details(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE id=?", (id,))
    course = cursor.fetchone()

    cursor.execute("SELECT * FROM videos WHERE course_id=?", (id,))
    videos = cursor.fetchall()

    conn.close()

    return render_template("course_details.html", course=course, videos=videos)


# ---------------- QUIZ ----------------

@app.route("/quiz/<int:course_id>")
def quiz(course_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes WHERE course_id=?", (course_id,))
    questions = cursor.fetchall()

    conn.close()

    return render_template("quiz.html", questions=questions, course_id=course_id)


# ---------------- SUBMIT QUIZ ----------------

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    if "user_id" not in session:
        return redirect("/login")

    data = request.json
    answers = data["answers"]
    course_id = data["course_id"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    score = 0
    total = len(answers)

    for qid, user_ans in answers.items():
        cursor.execute("SELECT correct_answer FROM quizzes WHERE id=?", (qid,))
        row = cursor.fetchone()

        if row and row[0] == user_ans:
            score += 1

    percentage = (score / total) * 100 if total > 0 else 0

    cursor.execute("""
    INSERT INTO quiz_results(user_id,course_id,score,total,percentage)
    VALUES (?,?,?,?,?)
    """, (session["user_id"], course_id, score, total, percentage))

    conn.commit()
    conn.close()

    return {"score": score, "total": total, "percentage": percentage}


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.execute("""
    SELECT courses.name, quiz_results.score, quiz_results.total, quiz_results.percentage
    FROM quiz_results
    JOIN courses ON quiz_results.course_id = courses.id
    WHERE quiz_results.user_id=?
    """, (session["user_id"],))

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        courses=courses,
        results=results
    )


# ---------------- NOTES ----------------

@app.route("/notes")
def notes():
    return render_template("notes.html")


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory("notes", filename)


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
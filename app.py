"""
====================================================================
          AI-POWERED FINANCIAL DOCUMENT ANALYSIS SYSTEM
====================================================================

Description
-----------
This Flask application is the main backend of the AI-Powered Financial
Document Analysis System. It provides a secure web interface for
analyzing payslips and bank statements using OCR and Machine Learning.

Main Features
-------------
• User registration and secure login using SQLite.
• OCR-based payslip text extraction and salary analysis.
• Loan eligibility prediction based on extracted salary.
• Bank statement transaction extraction and classification.
• Financial data visualization using pie charts and bar charts.
• Secure file upload and document management.

Modules
-------
• User Authentication
• Payslip OCR & Salary Extraction
• Loan Eligibility Checker
• Bank Statement Analysis
• Data Visualization
• SQLite Database Management

Technologies Used
-----------------
Python • Flask • SQLite • Tesseract OCR • Pandas
Matplotlib • OpenCV • NumPy • HTML • CSS • JavaScript

Author
------
Ritam Halder
B.Tech CSE (AI & ML)
The Neotia University

====================================================================
"""
from loan.loan_checker import check_loan_eligibility
from bank_statement.extractor import extract_bank_statement
from bank_statement.bar_chart import create_bar_chart
from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from bank_statement.charts import create_bar

from bank_statement.charts import create_pie

app = Flask(__name__)

from ocr.ocr import extract_text
from extraction.payslip_extractor import extract_salary
from charts.piechart import create_pie_chart

# ==========================
# Database Initialization
# ==========================

DATABASE = "database/users.db"

def init_db():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT

    )

    """)

    conn.commit()

    conn.close()


init_db()

# ==========================
# Home
# ==========================

@app.route("/")
def home():
    return render_template("login.html")


# ==========================
# Register Page
# ==========================

@app.route("/register")
def register():
    return render_template("register.html")


# ==========================
# Register User
# ==========================

@app.route("/register_user", methods=["POST"])
def register_user():

    username = request.form["username"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()

    try:

        cur.execute(

            "INSERT INTO users(username,password) VALUES(?,?)",

            (username, hashed_password)

        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        return "<h2>User already exists!</h2>"

    conn.close()

    return redirect("/")


# ==========================
# Login
# ==========================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()

    cur.execute(

        "SELECT password FROM users WHERE username=?",

        (username,)

    )

    user = cur.fetchone()

    conn.close()

    if user:

        if check_password_hash(user[0], password):

            return redirect("/dashboard")

    return "<h2>Invalid Username or Password</h2>"


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# ==========================
# Payslip Page
# ==========================

@app.route("/payslip")
def payslip():

    return render_template("payslip.html")


# ==========================
# Upload Payslip
# ==========================
@app.route("/upload_payslip", methods=["POST"])
def upload_payslip():

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    # OCR
    text = extract_text(filepath)

    # Salary Extraction
    salary = extract_salary(text)

    # Pie Chart
    create_pie_chart(salary)

    # Loan Eligibility
    salary = extract_salary(text)

    create_pie_chart(salary)

    status, color, income = check_loan_eligibility(salary)

    return render_template(
        "result.html",
        salary=salary,
        status=status,
        color=color,
        income=income
    )

# ==========================
# Bank Statement
# ==========================
# Bank Statement Page
# ==========================

@app.route("/bankstatement")
def bankstatement():

    return render_template("bankstatement.html")


# ==========================
# Upload Bank Statement
# ==========================

@app.route("/upload_bankstatement", methods=["POST"])
def upload_bankstatement():

    if "file" not in request.files:
        return "No File Uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No File Selected"

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    # -----------------------------
    # Extract Bank Statement
    # -----------------------------

    df = extract_bank_statement(filepath)
    create_bar(df)

    create_pie(df)

    if df.empty:
        return "<h2>No transaction data detected in the uploaded bank statement.</h2>"

    # -----------------------------
    # Generate Bar Chart
    # -----------------------------

    create_bar_chart(df)

    # -----------------------------
    # Display Result
    # -----------------------------

    return render_template(
        "bank_result.html",
        tables=df.to_dict(orient="records")
    )
# ==========================
# Run Flask
# ==========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
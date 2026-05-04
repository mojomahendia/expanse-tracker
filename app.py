from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        return render_template("register.html", error="Name is required")
    if not email or "@" not in email:
        return render_template("register.html", error="Enter a valid email address")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters")
    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match")

    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", (email,)
    ).fetchone()
    if existing:
        conn.close()
        return render_template("register.html", error="An account with that email already exists")

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password))
    )
    conn.commit()
    conn.close()

    flash("Account created! You can now sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return render_template("login.html", error="Email is required")
    if not password:
        return render_template("login.html", error="Password is required")

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You've been signed out.")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "April 2026",
    }
    stats = {
        "total_spent": "328.25",
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "Apr 25", "description": "Grocery run",   "category": "Food",          "amount": "22.00"},
        {"date": "Apr 22", "description": "Miscellaneous", "category": "Other",         "amount": "8.75"},
        {"date": "Apr 18", "description": "Clothing",      "category": "Shopping",      "amount": "65.00"},
        {"date": "Apr 14", "description": "Movie tickets", "category": "Entertainment", "amount": "20.00"},
        {"date": "Apr 10", "description": "Pharmacy",      "category": "Health",        "amount": "35.00"},
    ]
    categories = [
        {"name": "Bills",         "total": "120.00", "pct": 37},
        {"name": "Shopping",      "total": "65.00",  "pct": 20},
        {"name": "Transport",     "total": "45.00",  "pct": 14},
        {"name": "Health",        "total": "35.00",  "pct": 11},
        {"name": "Food",          "total": "34.50",  "pct": 11},
        {"name": "Entertainment", "total": "20.00",  "pct": 6},
        {"name": "Other",         "total": "8.75",   "pct": 3},
    ]
    return render_template("profile.html",
        user=user, stats=stats,
        transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

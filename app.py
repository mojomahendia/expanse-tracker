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
        "name":         "Arjun Sharma",
        "email":        "arjun@example.com",
        "member_since": "January 2025",
    }
    stats = {
        "total_spent":       "12,480.50",
        "transaction_count": 24,
        "top_category":      "Food & Dining",
    }
    expenses = [
        {"id": 1, "date": "Apr 30, 2026", "description": "Swiggy order",         "category": "Food",          "amount": 345.00},
        {"id": 2, "date": "Apr 28, 2026", "description": "Metro card recharge",  "category": "Transport",     "amount": 200.00},
        {"id": 3, "date": "Apr 25, 2026", "description": "Netflix subscription", "category": "Entertainment", "amount": 649.00},
        {"id": 4, "date": "Apr 22, 2026", "description": "Electricity bill",     "category": "Bills",         "amount": 1850.00},
        {"id": 5, "date": "Apr 18, 2026", "description": "Zara — spring haul",   "category": "Shopping",      "amount": 3200.00},
        {"id": 6, "date": "Apr 15, 2026", "description": "Grocery run",          "category": "Food",          "amount": 680.00},
    ]
    categories = [
        {"name": "Food",          "slug": "food",          "amount": "4,200.00", "pct": 34},
        {"name": "Bills",         "slug": "bills",         "amount": "3,600.00", "pct": 29},
        {"name": "Transport",     "slug": "transport",     "amount": "2,100.00", "pct": 17},
        {"name": "Shopping",      "slug": "shopping",      "amount": "1,580.00", "pct": 13},
        {"name": "Entertainment", "slug": "entertainment", "amount": "1,000.50", "pct": 8},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           expenses=expenses, categories=categories)


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

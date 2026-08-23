from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.user import db, User, GratitudeEntry, ManifestationEntry
from datetime import date, timedelta

from models.user import (
    db,
    User,
    GratitudeEntry,
    ManifestationEntry,
    VisionBoardItem
)

from datetime import date
from werkzeug.utils import secure_filename

import os
import uuid


# =========================================================
# CREATE APP
# =========================================================

app = Flask(__name__)


# =========================================================
# APP CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = "lumora-dev-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lumora.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================================
# VISION BOARD IMAGE UPLOAD CONFIGURATION
# =========================================================

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

app.config["ALLOWED_EXTENSIONS"] = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}


os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# =========================================================
# HELPER FUNCTION - CHECK IMAGE TYPE
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_EXTENSIONS"]
    )


# =========================================================
# INITIALIZE DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# LANDING PAGE
# =========================================================

@app.route("/")
def landing():

    return render_template(
        "landing.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        user_type = request.form.get(
            "user_type",
            ""
        )


        # Check empty fields

        if not all([
            name,
            email,
            password,
            confirm_password,
            user_type
        ]):

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Check password confirmation

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Check existing email

        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Create new user

        new_user = User(
            name=name,
            email=email,
            user_type=user_type
        )

        new_user.set_password(
            password
        )


        # Save user

        db.session.add(
            new_user
        )

        db.session.commit()


        flash(
            "Your Lumora account has been created ✨",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        # Find user

        user = User.query.filter_by(
            email=email
        ).first()


        # Check password

        if user and user.check_password(password):

            session["user_id"] = user.id

            session["user_name"] = user.name

            session["user_type"] = user.user_type


            flash(
                "Welcome back to Lumora ✨",
                "success"
            )


            return redirect(
                url_for("home")
            )


        flash(
            "Invalid email or password.",
            "error"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# HOME
# =========================================================

@app.route("/home")
def home():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = db.session.get(
        User,
        session["user_id"]
    )


    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )


    return render_template(
        "home.html",
        user=user
    )


# =========================================================
# RESET CENTER
# =========================================================

@app.route("/reset")
def reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "reset.html"
    )


# =========================================================
# STRESS RESET
# =========================================================

@app.route("/reset/stress")
def stress_reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "stress_reset.html"
    )


# =========================================================
# OVERWHELMED RESET
# =========================================================

@app.route("/reset/overwhelmed")
def overwhelmed_reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "overwhelmed_reset.html"
    )


# =========================================================
# FOCUS RESET
# =========================================================

@app.route("/reset/focus")
def focus_reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "focus_reset.html"
    )


# =========================================================
# TIRED RESET
# =========================================================

@app.route("/reset/tired")
def tired_reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "tired_reset.html"
    )


# =========================================================
# MOTIVATION RESET
# =========================================================

@app.route("/reset/motivation")
def motivation_reset():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "motivation_reset.html"
    )


# =========================================================
# BREATHE
# =========================================================

@app.route("/breathe")
def breathe():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "breathe.html"
    )


# =========================================================
# MEDITATE
# =========================================================

@app.route("/meditate")
def meditate():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "meditate.html"
    )


# =========================================================
# POMODORO
# =========================================================

@app.route("/pomodoro")
def pomodoro():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "pomodoro.html"
    )


# =========================================================
# GRATITUDE JOURNAL
# =========================================================

@app.route("/gratitude", methods=["GET", "POST"])
def gratitude():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    today = date.today()


    # -----------------------------------------------------
    # SAVE OR UPDATE GRATITUDE
    # -----------------------------------------------------

    if request.method == "POST":

        gratitude_one = request.form.get(
            "gratitude_one",
            ""
        ).strip()

        gratitude_two = request.form.get(
            "gratitude_two",
            ""
        ).strip()

        gratitude_three = request.form.get(
            "gratitude_three",
            ""
        ).strip()


        # Find today's existing entry

        entry = GratitudeEntry.query.filter_by(
            user_id=user_id,
            entry_date=today
        ).first()


        # Update existing entry

        if entry:

            entry.gratitude_one = gratitude_one

            entry.gratitude_two = gratitude_two

            entry.gratitude_three = gratitude_three


        # Create new entry

        else:

            entry = GratitudeEntry(
                user_id=user_id,
                gratitude_one=gratitude_one,
                gratitude_two=gratitude_two,
                gratitude_three=gratitude_three,
                entry_date=today
            )

            db.session.add(
                entry
            )


        # Save database

        db.session.commit()


        # Appreciation message

        flash(
            "✨ Your gratitude has been saved. Thank you for taking a moment to appreciate the beautiful little things in your life. 💛",
            "gratitude-success"
        )


        return redirect(
            url_for("gratitude")
        )


    # -----------------------------------------------------
    # LOAD TODAY'S SAVED GRATITUDE
    # -----------------------------------------------------

    entry = GratitudeEntry.query.filter_by(
        user_id=user_id,
        entry_date=today
    ).first()


    return render_template(
        "gratitude.html",
        entry=entry
    )


# =========================================================
# MANIFESTATION JOURNAL
# =========================================================

@app.route("/manifestation", methods=["GET", "POST"])
def manifestation():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    today = date.today()


    # -----------------------------------------------------
    # SAVE OR UPDATE MANIFESTATION
    # -----------------------------------------------------

    if request.method == "POST":

        dream = request.form.get(
            "dream",
            ""
        ).strip()

        feeling = request.form.get(
            "feeling",
            ""
        ).strip()

        life_description = request.form.get(
            "life_description",
            ""
        ).strip()

        affirmation = request.form.get(
            "affirmation",
            ""
        ).strip()


        # Find today's existing entry

        entry = ManifestationEntry.query.filter_by(
            user_id=user_id,
            entry_date=today
        ).first()


        # Update existing entry

        if entry:

            entry.dream = dream

            entry.feeling = feeling

            entry.life_description = life_description

            entry.affirmation = affirmation


        # Create new entry

        else:

            entry = ManifestationEntry(
                user_id=user_id,
                dream=dream,
                feeling=feeling,
                life_description=life_description,
                affirmation=affirmation,
                entry_date=today
            )

            db.session.add(
                entry
            )


        # Save database

        db.session.commit()


        # Appreciation message

        flash(
            "✦ Your manifestation has been saved. Keep believing in what you are creating and becoming. The universe is listening. ✨💜",
            "manifestation-success"
        )


        return redirect(
            url_for("manifestation")
        )


    # -----------------------------------------------------
    # LOAD TODAY'S SAVED MANIFESTATION
    # -----------------------------------------------------

    entry = ManifestationEntry.query.filter_by(
        user_id=user_id,
        entry_date=today
    ).first()


    return render_template(
        "manifestation.html",
        entry=entry
    )


# =========================================================
# VISION BOARD
# =========================================================

# =========================================================
# VISION BOARD
# =========================================================

@app.route("/vision-board", methods=["GET", "POST"])
def vision_board():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    # -----------------------------------------------------
    # SAVE NEW VISION BOARD ITEM
    # -----------------------------------------------------

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        affirmation = request.form.get(
            "affirmation",
            ""
        ).strip()

        image = request.files.get("image")

        # Basic validation

        if not title or not category:

            flash(
                "Please add a title and category for your vision.",
                "error"
            )

            return redirect(
                url_for("vision_board")
            )

        image_filename = None

        # -------------------------------------------------
        # SAVE IMAGE
        # -------------------------------------------------

        if image and image.filename != "":

            if allowed_file(image.filename):

                original_filename = secure_filename(
                    image.filename
                )

                unique_filename = (
                    str(uuid.uuid4())
                    + "_"
                    + original_filename
                )

                image.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        unique_filename
                    )
                )

                image_filename = unique_filename

            else:

                flash(
                    "Please upload a valid image file (PNG, JPG, JPEG, GIF or WEBP).",
                    "error"
                )

                return redirect(
                    url_for("vision_board")
                )

        # -------------------------------------------------
        # CREATE VISION BOARD ITEM
        # -------------------------------------------------

        new_item = VisionBoardItem(
            user_id=user_id,
            title=title,
            category=category,
            description=description,
            affirmation=affirmation,
            image_filename=image_filename
        )

        db.session.add(new_item)
        db.session.commit()

        flash(
            "✨ Your vision has been added to your board!",
            "success"
        )

        return redirect(
            url_for("vision_board")
        )

    # -----------------------------------------------------
    # LOAD USER'S VISION BOARD
    # -----------------------------------------------------

    items = VisionBoardItem.query.filter_by(
        user_id=user_id
    ).order_by(
        VisionBoardItem.created_at.desc()
    ).all()

    return render_template(
        "vision_board.html",
        items=items
    )

# =========================
# MY LUMORA DIARY
# =========================

@app.route("/diary")
def diary():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get the week requested in the URL
    week_start_string = request.args.get("week")

    # If no week is selected, show the current week
    if week_start_string:

        try:
            selected_date = date.fromisoformat(
                week_start_string
            )

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()


    # Monday = start of the week
    week_start = selected_date - timedelta(
        days=selected_date.weekday()
    )

    # Sunday = end of the week
    week_end = week_start + timedelta(
        days=6
    )


    # Get all gratitude entries for this week
    gratitude_entries = GratitudeEntry.query.filter(
        GratitudeEntry.user_id == user_id,
        GratitudeEntry.entry_date >= week_start,
        GratitudeEntry.entry_date <= week_end
    ).all()


    # Get all manifestation entries for this week
    manifestation_entries = ManifestationEntry.query.filter(
        ManifestationEntry.user_id == user_id,
        ManifestationEntry.entry_date >= week_start,
        ManifestationEntry.entry_date <= week_end
    ).all()


    # Create dictionaries using the date as the key
    gratitude_by_date = {
        entry.entry_date: entry
        for entry in gratitude_entries
    }

    manifestation_by_date = {
        entry.entry_date: entry
        for entry in manifestation_entries
    }


    # Create all 7 days of the selected week
    week_days = []

    for day_number in range(7):

        current_day = week_start + timedelta(
            days=day_number
        )

        week_days.append({

            "date": current_day,

            "gratitude": gratitude_by_date.get(
                current_day
            ),

            "manifestation": manifestation_by_date.get(
                current_day
            )

        })


    # Previous and next week
    previous_week = week_start - timedelta(
        days=7
    )

    next_week = week_start + timedelta(
        days=7
    )


    return render_template(
    "diary.html",
    week_days=week_days,
    week_start=week_start,
    week_end=week_end,
    previous_week=previous_week,
    next_week=next_week,
    today=date.today()
)
# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You've left your Lumora space. See you soon ✨",
        "success"
    )


    return redirect(
        url_for("landing")
    )


# =========================================================
# TYPOGRAPHY SHOWCASE
# =========================================================

@app.route("/typography")
def typography():

    return render_template(
        "typography.html"
    )


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
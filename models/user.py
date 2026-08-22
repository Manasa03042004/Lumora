from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


# =========================================================
# DATABASE
# =========================================================

db = SQLAlchemy()


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    user_type = db.Column(
        db.String(30),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    # Password methods

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


# =========================================================
# GRATITUDE JOURNAL MODEL
# =========================================================

class GratitudeEntry(db.Model):

    __tablename__ = "gratitude_entries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # Which user owns this gratitude entry?

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    # Today's 3 gratitude answers

    gratitude_one = db.Column(
        db.Text,
        nullable=True
    )

    gratitude_two = db.Column(
        db.Text,
        nullable=True
    )

    gratitude_three = db.Column(
        db.Text,
        nullable=True
    )


    # The actual day this journal belongs to

    entry_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )


    # When it was first created

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    # Relationship to User

    user = db.relationship(
        "User",
        backref="gratitude_entries"
    )


# =========================================================
# MANIFESTATION JOURNAL MODEL
# =========================================================

class ManifestationEntry(db.Model):

    __tablename__ = "manifestation_entries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # Which user owns this manifestation?

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    # What the user wants to manifest

    dream = db.Column(
        db.Text,
        nullable=True
    )


    # How the manifested life makes them feel

    feeling = db.Column(
        db.Text,
        nullable=True
    )


    # Description of their dream life

    life_description = db.Column(
        db.Text,
        nullable=True
    )


    # Personal manifestation affirmation

    affirmation = db.Column(
        db.Text,
        nullable=True
    )


    # The day this manifestation belongs to

    entry_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )


    # When it was first created

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    # Relationship to User

    user = db.relationship(
        "User",
        backref="manifestation_entries"
    )

    # =========================================================
# VISION BOARD MODEL
# =========================================================

class VisionBoardItem(db.Model):

    __tablename__ = "vision_board_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Which user owns this vision item
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Vision details
    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    affirmation = db.Column(
        db.Text,
        nullable=True
    )

    # Stores uploaded image filename
    image_filename = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationship to User
    user = db.relationship(
        "User",
        backref="vision_board_items"
    )
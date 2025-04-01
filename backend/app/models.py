from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"




class Article(db.Model):
    """Represents a full Wikipedia article with internal links and metadata."""
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), unique=True, nullable=False)
    full_text = db.Column(db.Text, nullable=False)
    internal_links = db.Column(db.Text)
    retrieved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article topic='{self.topic}'>"

class Links(db.Model):
    """Stores individual internal Wikipedia links related to a topic."""
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), db.ForeignKey("articles.topic"), nullable=False)
    linked_topic = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Link topic='{self.topic}' linked_to='{self.linked_topic}'>"

class Summary(db.Model):
    """Stores summaries of a topic at basic, intermediate, and advanced levels."""
    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), db.ForeignKey('articles.topic'), unique=True, nullable=False)
    basic_summary = db.Column(db.Text)
    intermediate_summary = db.Column(db.Text)
    advanced_summary = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Summary topic='{self.topic}'>"

class LearningPath(db.Model):
    """Stores a ranked set of internal links for a topic."""
    __tablename__ = "learning_paths"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), db.ForeignKey("articles.topic"), nullable=False)
    ranked_links = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LearningPath topic='{self.topic}'>"

class CanonicalTopic(db.Model):
    """Maps user input to resolved Wikipedia canonical topic titles."""
    __tablename__ = "canonical_topics"

    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(255), unique=True, nullable=False)
    canonical_title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<CanonicalTopic '{self.user_input}' => '{self.canonical_title}'>"

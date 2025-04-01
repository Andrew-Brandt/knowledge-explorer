import json
import logging
from datetime import datetime
from app import db
from app.models import Article, Links, Summary, LearningPath, CanonicalTopic, User

logger = logging.getLogger(__name__)




def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    return User.query.get(int(user_id))  # Used by Flask-Login's user_loader

def create_user(username, email, password, is_admin=False):
    if get_user_by_username(username) or get_user_by_email(email):
        logger.warning(f"Attempted to create duplicate user: {username}")
        return None  # User already exists

    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)

    try:
        db.session.commit()
        logger.info(f"New user created: {username}")
        return user
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create user '{username}': {e}")
        return None

def verify_user_credentials(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None

def is_admin_user(user):
    return user.is_authenticated and user.is_admin









def store_article_in_db(canonical_topic, content):
    article = Article.query.filter_by(topic=canonical_topic).first()

    if article:
        logger.info(f"Updating existing article: {canonical_topic}")
        article.full_text = content
    else:
        logger.info(f"Storing new article: {canonical_topic}")
        article = Article(topic=canonical_topic, full_text=content)
        db.session.add(article)

    try:
        db.session.commit()
        logger.info(f"Article stored: {canonical_topic}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store article '{canonical_topic}': {e}")

def get_article_from_db(topic):
    article = Article.query.filter_by(topic=topic).first()
    return article.full_text if article else None

def store_links_in_db(canonical_topic, links):
    existing_entry = Links.query.filter_by(topic=canonical_topic).first()

    if existing_entry:
        logger.info(f"Updating links for {canonical_topic}")
        existing_entry.linked_topic = json.dumps(links)
    else:
        logger.info(f"Storing new links for {canonical_topic}")
        new_entry = Links(topic=canonical_topic, linked_topic=json.dumps(links))
        db.session.add(new_entry)

    try:
        db.session.commit()
        logger.info(f"Links stored for {canonical_topic}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store links for '{canonical_topic}': {e}")

def get_links_from_db(topic):
    entry = Links.query.filter_by(topic=topic).first()
    return json.loads(entry.linked_topic) if entry and entry.linked_topic else []


def store_summaries_in_db(canonical_topic, summaries_dict):
    existing = Summary.query.filter_by(topic=canonical_topic).first()

    if existing:
        logger.info(f"Updating summaries for '{canonical_topic}'")
        existing.basic_summary = summaries_dict.get("basic")
        existing.intermediate_summary = summaries_dict.get("intermediate")
        existing.advanced_summary = summaries_dict.get("advanced")
        existing.generated_at = datetime.utcnow()
    else:
        logger.info(f"Storing new summaries for '{canonical_topic}'")
        new_entry = Summary(
            topic=canonical_topic,
            basic_summary=summaries_dict.get("basic"),
            intermediate_summary=summaries_dict.get("intermediate"),
            advanced_summary=summaries_dict.get("advanced"),
            generated_at=datetime.utcnow()
        )
        db.session.add(new_entry)

    try:
        db.session.commit()
        logger.info(f"Summaries stored for '{canonical_topic}'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store summaries for '{canonical_topic}': {e}")

def get_summary_from_db(topic, level):
    summary = Summary.query.filter_by(topic=topic).first()
    if not summary:
        return None
    return {
        "basic": summary.basic_summary,
        "intermediate": summary.intermediate_summary,
        "advanced": summary.advanced_summary,
    }.get(level)

def store_learning_path_in_db(canonical_topic, ranked_links):
    existing_path = LearningPath.query.filter_by(topic=canonical_topic).first()
    json_data = json.dumps(ranked_links)

    if existing_path:
        logger.info(f"Updating learning path for '{canonical_topic}'")
        existing_path.ranked_links = json_data
        existing_path.last_updated = datetime.utcnow()
    else:
        logger.info(f"Storing new learning path for '{canonical_topic}'")
        new_learning_path = LearningPath(
            topic=canonical_topic,
            ranked_links=json_data,
            last_updated=datetime.utcnow()
        )
        db.session.add(new_learning_path)

    try:
        db.session.commit()
        logger.info(f"Learning path stored for '{canonical_topic}'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store learning path for '{canonical_topic}': {e}")

def get_learning_path_from_db(topic):
    learning_path = LearningPath.query.filter_by(topic=topic).first()
    if not learning_path:
        logger.warning(f"No learning path found in DB for '{topic}'.")
        return None
    return json.loads(learning_path.ranked_links) if learning_path.ranked_links else []

def store_canonical_topic_in_db(user_input, canonical_title):
    existing = CanonicalTopic.query.filter_by(user_input=user_input).first()
    if existing:
        existing.canonical_title = canonical_title
    else:
        new_entry = CanonicalTopic(user_input=user_input, canonical_title=canonical_title)
        db.session.add(new_entry)

    try:
        db.session.commit()
        logger.info(f"Canonical topic stored in db: '{user_input}' -> '{canonical_title}'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store canonical topic mapping for '{user_input}': {e}")

def get_canonical_topic_from_db(user_input):
    entry = CanonicalTopic.query.filter_by(user_input=user_input).first()
    return entry.canonical_title if entry else None

def initialize_database():
    db.create_all()
    logger.info("Database tables initialized.")

def clear_database():
    logger.warning("Clearing all database records...")
    db.session.query(Article).delete()
    db.session.query(Links).delete()
    db.session.query(Summary).delete()
    db.session.query(LearningPath).delete()
    db.session.query(CanonicalTopic).delete()
    db.session.commit()
    logger.info("Database has been cleared!")

if __name__ == "__main__":
    initialize_database()

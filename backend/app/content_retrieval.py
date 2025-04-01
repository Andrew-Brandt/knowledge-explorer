import json
import logging

from app.database import (
    get_article_from_db,
    store_article_in_db,
    get_summary_from_db,
    store_summaries_in_db,
    get_links_from_db,
    store_links_in_db,
    get_learning_path_from_db,
    store_learning_path_in_db,
    get_canonical_topic_from_db,
    store_canonical_topic_in_db
)
from app.cache import (
    get_article_from_cache,
    store_article_in_cache,
    get_links_from_cache,
    store_links_in_cache,
    get_summary_from_cache,
    store_summaries_in_cache,
    get_learning_path_from_cache,
    store_learning_path_in_cache,
    get_canonical_topic_from_cache,
    store_canonical_topic_in_cache
)
from app.llm import summarize_text, rank_learning_path
from app.wikipedia import get_wiki_html
from app.utils import slice_links_by_level, deduplicate_learning_path


logger = logging.getLogger(__name__)

def get_canonical_topic(user_input):
    canonical = get_canonical_topic_from_cache(user_input)
    if canonical:
        return canonical

    canonical = get_canonical_topic_from_db(user_input)
    if canonical:
        store_canonical_topic_in_cache(user_input, canonical)
        return canonical

    canonical = get_wiki_html(user_input)
    if not canonical:
        return None

    return get_canonical_topic_from_cache(user_input) or get_canonical_topic_from_db(user_input)

def get_article_text(topic):
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return None

    cached_text = get_article_from_cache(canonical_topic)
    if cached_text:
        return cached_text

    db_text = get_article_from_db(canonical_topic)
    if db_text:
        return db_text

    soup = get_wiki_html(canonical_topic)
    if not soup:
        return None

    return get_article_from_cache(canonical_topic) or get_article_from_db(canonical_topic)

def get_article_summary(topic, level="basic"):
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return None

    cached_summary = get_summary_from_cache(canonical_topic, level)
    if cached_summary:
        return cached_summary

    db_summary = get_summary_from_db(canonical_topic, level)
    if db_summary:
        return db_summary

    article_text = get_article_text(canonical_topic)
    if not article_text:
        logger.warning(f"No article text found for topic '{canonical_topic}'")
        return None

    summaries = summarize_text(article_text)
    if not summaries:
        logger.error(f"Summarization failed for topic '{canonical_topic}'")
        return None

    store_summaries_in_cache(canonical_topic, summaries)
    store_summaries_in_db(canonical_topic, summaries)
    logger.info(f"Generated and stored summaries for topic '{canonical_topic}'")

    return summaries.get(level)

def get_article_links(topic):
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return []

    cached_links = get_links_from_cache(canonical_topic)
    if cached_links:
        return cached_links

    db_links = get_links_from_db(canonical_topic)
    if db_links:
        return db_links

    soup = get_wiki_html(canonical_topic)
    if not soup:
        return []

    return get_links_from_cache(canonical_topic) or get_links_from_db(canonical_topic)

def get_learning_path(topic: str, level: str) -> list:
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return []

    cached_path = get_learning_path_from_cache(canonical_topic)
    if cached_path:
        return cached_path

    db_path = get_learning_path_from_db(canonical_topic)
    if db_path:
        return db_path

    links = get_article_links(canonical_topic)
    summary = get_article_summary(canonical_topic)
    ranked = rank_learning_path(canonical_topic, links, summary)

    unique_ranked = deduplicate_learning_path(ranked, canonical_topic)

    store_learning_path_in_cache(canonical_topic, unique_ranked)
    store_learning_path_in_db(canonical_topic, unique_ranked)
    logger.info(f"Generated and stored learning path for topic '{canonical_topic}'")

    return unique_ranked



def regenerate_learning_path(topic):
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return []

    links = get_article_links(canonical_topic)
    summary = get_article_summary(canonical_topic)
    ranked = rank_learning_path(canonical_topic, links, summary)

    unique_ranked = deduplicate_learning_path(ranked, canonical_topic)

    store_learning_path_in_cache(canonical_topic, unique_ranked)
    store_learning_path_in_db(canonical_topic, unique_ranked)
    logger.info(f"Regenerated and stored learning path for topic '{canonical_topic}'")

    return unique_ranked


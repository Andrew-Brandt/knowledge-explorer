import redis
import json
import logging

logger = logging.getLogger(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_from_cache(key: str):
    try:
        return redis_client.get(key)
    except redis.exceptions.RedisError as e:
        logger.error(f"Redis GET failed for key '{key}': {e}")
        return None

def store_in_cache(key: str, value, expiration: int = 86400):
    try:
        redis_client.set(key, value, ex=expiration)
    except redis.exceptions.RedisError as e:
        logger.error(f"Redis SET failed for key '{key}': {e}")

def invalidate_cache(topic: str):
    keys = [
        f"article:{topic}", f"links:{topic}",
        f"summary:{topic}:basic", f"summary:{topic}:intermediate", f"summary:{topic}:advanced",
        f"learning_path:{topic}", f"canonical:{topic.lower()}"
    ]
    for key in keys:
        try:
            redis_client.delete(key)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis DELETE failed for key '{key}': {e}")
    logger.info(f"Cache invalidated for topic '{topic}'")

def clear_cache():
    try:
        redis_client.flushdb()
        logger.warning("Entire cache cleared.")
    except redis.exceptions.RedisError as e:
        logger.error(f"Redis FLUSHDB failed: {e}")

def store_article_in_cache(topic: str, content: str, expiration: int = 86400):
    store_in_cache(f"article:{topic}", content, expiration)

def get_article_from_cache(topic: str):
    return get_from_cache(f"article:{topic}")

def store_links_in_cache(topic: str, links, expiration: int = 86400):
    try:
        store_in_cache(f"links:{topic}", json.dumps(links), expiration)
    except (TypeError, redis.exceptions.RedisError) as e:
        logger.error(f"Failed to store links for topic '{topic}': {e}")

def get_links_from_cache(topic: str):
    links = get_from_cache(f"links:{topic}")
    try:
        return json.loads(links) if links else None
    except json.JSONDecodeError:
        logger.error(f"Corrupted cache entry for links:{topic}")
        return None

def store_summaries_in_cache(topic: str, summaries_dict: dict, expiration: int = 86400):
    for level, summary in summaries_dict.items():
        store_in_cache(f"summary:{topic}:{level}", summary, expiration)

def get_summary_from_cache(topic: str, level: str):
    return get_from_cache(f"summary:{topic}:{level}")

def store_learning_path_in_cache(topic: str, ranked_links, expiration: int = 86400):
    try:
        store_in_cache(f"learning_path:{topic}", json.dumps(ranked_links), expiration)
    except (TypeError, redis.exceptions.RedisError) as e:
        logger.error(f"Failed to store learning path for topic '{topic}': {e}")

def get_learning_path_from_cache(topic: str):
    cached_path = get_from_cache(f"learning_path:{topic}")
    try:
        return json.loads(cached_path) if cached_path else None
    except json.JSONDecodeError:
        logger.error(f"Corrupted cache entry for learning_path:{topic}")
        return None

def get_canonical_topic_from_cache(user_input: str):
    try:
        return redis_client.get(f"canonical:{user_input.lower()}")
    except redis.exceptions.RedisError as e:
        logger.error(f"Redis GET failed for canonical topic '{user_input}': {e}")
        return None

def store_canonical_topic_in_cache(user_input: str, resolved_title: str):
    try:
        redis_client.set(f"canonical:{user_input.lower()}", resolved_title)
    except redis.exceptions.RedisError as e:
        logger.error(f"Redis SET failed for canonical topic '{user_input}': {e}")

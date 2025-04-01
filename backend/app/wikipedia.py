import requests
import logging
from bs4 import BeautifulSoup
from app.utils import sanitize_wiki_intro, sanitize_wiki_links
from app.cache import (
    store_article_in_cache,
    store_links_in_cache,
    store_canonical_topic_in_cache
)
from app.database import (
    store_article_in_db,
    store_links_in_db,
    store_canonical_topic_in_db
)

logger = logging.getLogger(__name__)

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "WikiTutorBot/1.0 (andy.n.brandt@gmail.com)",
    "Accept-Encoding": "gzip"
}

def get_wiki_html(topic):

    params = {
        "action": "parse",
        "format": "json",
        "page": topic,
        "prop": "text",
        "redirects": 1
    }
    try:
        response = requests.get(WIKI_API_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if "parse" not in data:
            logger.warning(f"Wikipedia parse block missing for '{topic}'")
            return None, None

        html = BeautifulSoup(data["parse"]["text"]["*"], "lxml")
        canonical_title = data["parse"].get("title", topic)

        # Cache + DB store: canonical title
        store_canonical_topic_in_cache(topic, canonical_title)
        store_canonical_topic_in_db(topic, canonical_title)

        # Extract and store intro
        intro_text = extract_intro_from_soup(html)
        if intro_text:
            store_article_in_cache(canonical_title, intro_text)
            store_article_in_db(canonical_title, intro_text)

        # Extract and store links
        links = extract_links_from_soup(html)
        if links:
            store_links_in_cache(canonical_title, links)
            store_links_in_db(canonical_title, links)

        return canonical_title

    except requests.RequestException as e:
        logger.error(f"Wikipedia API error for '{topic}': {e}")
        return None

def extract_links_from_soup(soup):
    content_div = soup.select_one("div.mw-parser-output")
    if not content_div:
        return []

    # If the page has only one paragraph and several <ul> lists, likely a disambiguation-style page
    if len(content_div.find_all("p", recursive=False)) <= 2:
        link_set = {
            a["href"].split("/wiki/")[-1].split("#")[0]
            for ul in content_div.find_all("ul", recursive=False)
            for li in ul.find_all("li")
            for a in li.find_all("a", href=True)
            if a["href"].startswith("/wiki/") and ":" not in a["href"]
        }
        return sanitize_wiki_links(list(link_set))

    # Normal page: extract links from paragraphs
    seen_links = {
        a["href"].split("/wiki/")[-1].split("#")[0]
        for p in content_div.find_all("p", recursive=False)
        for a in p.find_all("a", href=True)
        if a["href"].startswith("/wiki/") and ":" not in a["href"]
    }

    return sanitize_wiki_links(list(seen_links))

def extract_intro_from_soup(soup):
    content_div = soup.select_one("div.mw-parser-output")
    if not content_div:
        return None

    intro_text = []
    for element in content_div.children:
        if element.name == "div" and "mw-heading2" in element.get("class", []):
            break
        if element.name == "p" and element.text.strip():
            intro_text.append(str(element))

    if not intro_text:
        return None

    raw_html = "\n".join(intro_text)
    return sanitize_wiki_intro(raw_html)



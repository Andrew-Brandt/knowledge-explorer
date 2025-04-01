import re
import json
import logging
import markdownify
from urllib.parse import unquote
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_json_from_text(response_text: str):
    """Extract and sanitize JSON from raw response text (can be dict or list)."""
    json_start = response_text.find("{")
    json_end = response_text.rfind("}")

    if json_start == -1 or json_end == -1:
        json_start = response_text.find("[")
        json_end = response_text.rfind("]")
        if json_start == -1 or json_end == -1:
            logger.warning("No valid JSON object or array found in the response text.")
            return None

    raw_json_text = response_text[json_start:json_end + 1]

    # Fix known common escape issues
    raw_json_text = raw_json_text.replace('\"', '"')  # decode pre-escaped quotes

    # Replace escaped double quotes inside values with placeholder before fixing
    raw_json_text = re.sub(r'(?<!\\)"(?=[^"]*?\":)', '"', raw_json_text)  # make sure inner quotes stay

    # Remove invalid trailing commas
    raw_json_text = re.sub(r',\s*([}\]])', r'\1', raw_json_text)

    # Remove extra whitespace and line breaks
    raw_json_text = re.sub(r'\s+', ' ', raw_json_text).strip()

    try:
        return json.loads(raw_json_text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parsing Failed: {e}")
        logger.debug(f"Processed JSON Response: {raw_json_text}")
        return None

def sanitize_wiki_intro(html_text: str) -> str:
    """
    Convert HTML to markdown and clean Wikipedia intro text:
    - Converts HTML to markdown
    - Removes markdown links, bold/italic, footnotes, and citation anchors
    - Fixes spacing
    - Strips quotes and makes text plain
    """
    if not html_text:
        return ""

    markdown_text = markdownify.markdownify(html_text, heading_style="ATX")

    # Remove footnote references like [1], [2]
    markdown_text = re.sub(r"\[\d+\]", "", markdown_text)

    # Remove citation anchors like [](#cite_note-1)
    markdown_text = re.sub(r"\[\]\(#cite_note-[^\)]+\)", "", markdown_text)

    # Remove markdown links [text](url) -> text
    markdown_text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", markdown_text)
    # Deduplicate word pairs like "Title Title (Link)"
    markdown_text = re.sub(r'\b(\w+)\s+\1\b', r'\1', markdown_text)

    # Remove bold (**text**) and italic (*text*) markdown
    markdown_text = re.sub(r"\*\*(.*?)\*\*", r"\1", markdown_text)
    markdown_text = re.sub(r"\*(.*?)\*", r"\1", markdown_text)

    # Remove all single and double quotes
    markdown_text = markdown_text.replace("\"", "").replace("'", "")

    # Fix spacing
    markdown_text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', markdown_text)
    markdown_text = re.sub(r"\s+", " ", markdown_text).strip()

    logger.info("Wikipedia intro sanitized and converted from HTML.")
            # Remove duplicate closing parentheses like '))' -> ')'
    markdown_text = re.sub(r'\)\)+', ')', markdown_text)

    return unquote(markdown_text)

def sanitize_wiki_links(links):
    """Decode URL-encoded internal Wikipedia links."""
    logger.info("Wikipedia links sanitized")
    return [unquote(link) for link in links] if links else []



def slice_links_by_level(links, level):
    if not links:
        return []
    return {
        "basic": links[:6],
        "intermediate": links[:8],
        "advanced": links[:10]
    }.get(level, [])


def deduplicate_learning_path(ranked_links: list, main_topic: str) -> list:
    """
    Remove duplicates from the ranked links list based on their canonical topic.
    Explicitly exclude the main topic (or its canonical form) from the final list.
    """
    from app.content_retrieval import get_canonical_topic

    unique_links = []
    seen = set()

    canonical_main = get_canonical_topic(main_topic)
    if canonical_main:
        seen.add(canonical_main)

    for link in ranked_links:
        resolved = get_canonical_topic(link)
        if not resolved or resolved in seen:
            continue
        seen.add(resolved)
        unique_links.append(resolved)

    return unique_links




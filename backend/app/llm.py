import os
import re
import time
import json
import logging
from datetime import datetime
from typing import Optional

import anthropic
from app.utils import extract_json_from_text

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def rank_learning_path(topic: str, links: list, summary: str):
    if not links:
        logger.warning(f"No links provided for topic '{topic}'. Returning empty learning path.")
        return {"ranked": []}

    links_text = json.dumps(links)

    system_prompt = (
        "You are an expert curator tasked with creating an optimal learning path for a given topic using Wikipedia articles. "
        "Your goal is to select the 20 most important and informative Wikipedia article that will provide a comprehensive understanding of the subject."
        "Remember: you must choose only from the provided list of Wikipedia articles."

    )

    user_prompt = f"""
Here is the topic you need to analyze:

<topic>
{topic}
</topic>

To help you understand the context, here's a brief summary of the topic:

<summary>
{summary}
</summary>

Below is a list of Wikipedia article titles related to the topic. Your task is to select the 20 most relevant and informative articles from this list:

<links>
{links_text}
</links>

Instructions:
1. Carefully analyze the topic, summary, and list of links.
2. Identify the main subject and its key subtopics.
3. Select the 20 most important articles that will provide a comprehensive understanding of the topic. Consider the following criteria:
   - Core concept articles that directly explain the main topic
   - Key subtopics that are essential to understanding the subject
   - Related organizations or entities that play a significant role in the topic
   - Historical context or background information
   - Important processes or methods related to the topic
4. Ensure that the selected articles form a logical learning progression, from foundational concepts to more advanced details.
5. Do not include more than 20 links in your final output.
6. Only exact links in original list of Wikipedia articles are allowed.

provide your final selection of 20 links in the specified JSON format.
Ensure no additional text is included.
All article links must be a subset of the original list of links.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature= 0,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    logger.debug(f"LLM raw response: {response.content[0].text}")

    try:
        ranked_links = extract_json_from_text(response.content[0].text)

        if isinstance(ranked_links, dict):
            for key, value in ranked_links.items():
                if isinstance(value, list):
                    logger.info(f"Auto-detected list under key '{key}' in LLM response.")
                    ranked_links = value
                    break

        if not isinstance(ranked_links, list):
            raise ValueError("Expected a list of links from LLM response")

        logger.info(f"Successfully ranked learning path for topic '{topic}'.")
        return ranked_links
    except (json.JSONDecodeError, AttributeError, ValueError) as e:
        logger.error(f"Error parsing ranked links JSON: {e}")
        return None

def summarize_text(text):
    system_prompt = (
        "You are an AI assistant specialized in summarizing complex Wikipedia articles at different reading levels. "
        "Your task is to create three summaries of varying complexity for the given article. "
        "If the article is too short or lacks detail, enrich it using your background knowledge to provide a more informative summary. "
        "Remember:"
        "- Do not include markdown syntax. "
        "- Do not wrap the entire JSON in triple backticks. "
        "- Ensure the output can be safely parsed using json.loads()."
    )

    user_prompt = f"""
Here is the Wikipedia article you need to summarize:

<article>
{text}
</article>

Please analyze this article and create three summaries of the topic at different levels of complexity:

1. Basic (for young learners in grades 1-3)
2. Intermediate (for high school students in grades 7-12)
3. Advanced (for readers at the master's degree level)

Break down the article, identify key concepts, and plan your approach for each summary level. Include the following:

1. Key Concepts: The main topics and ideas from the article.
2. Complexity Assessment: Rate each concept as basic, intermediate, or advanced.
3. Vocabulary: Identify key terms that may need simplification or explanation at different levels.
4. Structure: Outline the article's structure to maintain a logical flow in summaries.
5. Audience Considerations: Note specific ways to adapt content for each audience level.

This will help ensure a thorough interpretation of the data and appropriate adaptation for each audience.

Guidelines for each summary level:

Basic:
- Use simple words and short sentences.
- Focus on core concepts and main ideas.
- Provide clear, engaging explanations.
- Use relatable examples or comparisons if needed.
- Aim for a length of 3-5 sentences.

Intermediate:
- Maintain key ideas and important details.
- Simplify technical terms, but introduce some field-specific vocabulary.
- Use a conversational yet informative tone.
- Assume some background knowledge, but explain advanced concepts.
- Aim for a length of 5-8 sentences.

Advanced:
- Preserve complex terminology and provide precise explanations where needed.
- Focus on deeper insights, nuanced interpretations, and contextual significance.
- Use formal, structured language aligned with academic standards.
- Assume foundational knowledge in the subject.
- Aim for a length of 8-12 sentences.

Present your summaries in a JSON object with "basic", "intermediate", and "advanced" keys.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        temperature=0.7,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    try:
        content_text = response.content[0].text if isinstance(response.content, list) else response.content
        json_text = extract_json_from_text(content_text)

        if isinstance(json_text, dict):
            summaries_dict = json_text
        else:
            summaries_dict = json.loads(json_text)

        logger.info(f"Successfully parsed summaries for levels: {list(summaries_dict.keys())}")
        return summaries_dict

    except (json.JSONDecodeError, ValueError, AttributeError, TypeError) as e:
        logger.error(f"Error parsing response JSON: {e}")
        logger.debug(f"Unexpected LLM response structure: {response.content}")
        return None

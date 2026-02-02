# Data Cleaning
# Cleans article data: whitespace, HTML, encoding, dates, control characters.

import html
import json
import re
from datetime import datetime


# Invisible / problematic characters to replace with normal space (e.g. non-breaking space).
INVISIBLE_TO_SPACE = (
    "\u00a0",   # no-break space
    "\u200b",   # zero width space
    "\u200c",   # zero width non-joiner
    "\u200d",   # zero width joiner
    "\ufeff",   # BOM
)


def clean_text(value):
    """
    Clean a string: strip and collapse whitespace, remove HTML tags and entities,
    normalize invisible characters, remove control characters. Keeps © ® ™.
    Returns empty string if value is not a string.
    """
    if value is None or not isinstance(value, str):
        return ""

    s = value

    # Replace problematic invisible characters with normal space
    for char in INVISIBLE_TO_SPACE:
        s = s.replace(char, " ")

    # Decode HTML entities (e.g. &nbsp; &amp; &quot;) to plain text
    s = html.unescape(s)

    # Remove HTML tags (e.g. <p>, <br>, <h1>)
    s = re.sub(r"<[^>]+>", "", s)

    # Strip leading/trailing whitespace and collapse internal whitespace to single space
    s = re.sub(r"\s+", " ", s).strip()

    # Remove ASCII control characters (keep tab, newline, carriage return)
    s = "".join(
        c for c in s
        if ord(c) >= 32 or c in "\t\n\r"
    )
    # Remove DEL (0x7f)
    s = "".join(c for c in s if ord(c) != 127)

    return s


def parse_date_to_iso(date_str):
    """
    Try to parse a date string into ISO 8601 format (YYYY-MM-DD or full ISO).
    If parsing fails, returns "".
    """
    if not date_str or not isinstance(date_str, str):
        return ""

    s = date_str.strip()
    if not s:
        return ""

    # Try ISO format first (e.g. 2026-02-02T02:30:50-05:00)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.isoformat()
    except (ValueError, TypeError):
        pass

    # Try "2026-Feb-01T13:28:27-05:00" style (month name)
    try:
        dt = datetime.strptime(s[:20], "%Y-%b-%dT%H:%M:%S")
        iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
        if len(s) > 20 and s[20] in "-+" and len(s) >= 26:
            iso += s[20:26] if len(s) > 25 and s[23] == ":" else s[20:23] + ":" + s[23:25]
        return iso
    except (ValueError, TypeError):
        pass

    # Try "Updated Jan. 26, 2026" or "Jan. 26, 2026"
    prefix_removed = re.sub(r"^Updated\s+", "", s, flags=re.IGNORECASE).strip()
    for candidate in (prefix_removed, s):
        try:
            dt = datetime.strptime(candidate, "%b. %d, %Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            try:
                dt = datetime.strptime(candidate, "%B %d, %Y")
                return dt.strftime("%Y-%m-%dT%H:%M:%S")
            except (ValueError, TypeError):
                pass

    return ""


def clean_article(article):
    """
    Clean one article dict: url, title, content, published.
    Preserves all keys; missing fields become empty strings. Never removes the record.
    """
    if not isinstance(article, dict):
        return article

    url = article.get("url")
    if url is None:
        url = ""
    elif isinstance(url, str):
        url = clean_text(url)
    else:
        url = str(url)

    title = clean_text(article.get("title"))
    content = clean_text(article.get("content"))
    published = article.get("published")
    if published is not None and isinstance(published, str):
        published = parse_date_to_iso(published)
    else:
        published = ""

    return {
        "url": url,
        "title": title,
        "content": content,
        "published": published,
    }


def clean(data):
    """
    Clean full input data (dict with 'generated_at' and 'articles').
    Same number of records; preserves structure. Output is UTF-8 safe.
    """
    if not isinstance(data, dict):
        return data

    generated_at = data.get("generated_at")
    if generated_at is None:
        generated_at = ""
    elif not isinstance(generated_at, str):
        generated_at = str(generated_at)

    articles = data.get("articles")
    if not isinstance(articles, list):
        articles = []

    cleaned_articles = [clean_article(a) for a in articles]

    return {
        "generated_at": clean_text(generated_at) or generated_at,
        "articles": cleaned_articles,
    }


def main():
    input_path = "sample_data.json"
    output_path = "cleaned_output.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = clean(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Cleaned {len(cleaned['articles'])} articles -> {output_path}")


if __name__ == "__main__":
    main()

# Data Validation
# Validates cleaned_output.json and writes quality_report.txt.

import json
from collections import Counter


def _strip(value):
    """Return stripped string if value is a string, else empty string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def validate_record(record):
    """
    Validate one record. Returns (is_valid, errors).
    errors is a list of reason codes: missing_title, missing_content, missing_url,
    invalid_url, content_too_short.
    """
    errors = []

    if not isinstance(record, dict):
        return False, ["invalid_record"]

    title = _strip(record.get("title"))
    content = _strip(record.get("content"))
    url = _strip(record.get("url"))

    if not title:
        errors.append("missing_title")
    if not content:
        errors.append("missing_content")
    if not url:
        errors.append("missing_url")

    if url and not (url.startswith("http://") or url.startswith("https://")):
        errors.append("invalid_url")

    if content and len(content) < 50:
        errors.append("content_too_short")

    is_valid = len(errors) == 0
    return is_valid, errors


def _is_present(record, key):
    """True if key exists and stripped value is not empty."""
    val = record.get(key)
    return bool(_strip(val))


def validate(data):
    """
    Validate all records in data (dict with 'articles' list).
    Returns dict with total_records, valid_count, invalid_count,
    title_present_count, content_present_count, url_present_count, date_present_count,
    completeness percentages, and error_counts.
    """
    articles = data.get("articles", [])
    if not isinstance(articles, list):
        articles = []

    total = len(articles)
    valid_count = 0
    invalid_count = 0
    title_present_count = 0
    content_present_count = 0
    url_present_count = 0
    date_present_count = 0
    error_counts = Counter()

    for record in articles:
        if _is_present(record, "title"):
            title_present_count += 1
        if _is_present(record, "content"):
            content_present_count += 1
        if _is_present(record, "url"):
            url_present_count += 1
        if _is_present(record, "published"):
            date_present_count += 1

        is_valid, errors = validate_record(record)
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            for e in errors:
                error_counts[e] += 1

    title_percent = round(100.0 * title_present_count / total, 2) if total else 0
    content_percent = round(100.0 * content_present_count / total, 2) if total else 0
    url_percent = round(100.0 * url_present_count / total, 2) if total else 0
    date_percent = round(100.0 * date_present_count / total, 2) if total else 0

    return {
        "total_records": total,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "title_present_count": title_present_count,
        "content_present_count": content_present_count,
        "url_present_count": url_present_count,
        "date_present_count": date_present_count,
        "title_percent": title_percent,
        "content_percent": content_percent,
        "url_percent": url_percent,
        "date_percent": date_percent,
        "error_counts": dict(error_counts),
    }


def write_report(result, output_path):
    """Write quality_report.txt in the required format."""
    lines = [
        "======================",
        "DATA QUALITY REPORT",
        "======================",
        f"Total records processed: {result['total_records']}",
        f"Valid records: {result['valid_count']}",
        f"Invalid records: {result['invalid_count']}",
        "",
        "----------------------",
        "Completeness Summary",
        "----------------------",
        f"Title completeness: {result['title_percent']}%",
        f"Content completeness: {result['content_percent']}%",
        f"URL completeness: {result['url_percent']}%",
        f"Date completeness: {result['date_percent']}%",
        "",
        "----------------------",
        "Common validation failures",
        "----------------------",
    ]

    error_counts = result["error_counts"]
    sorted_errors = sorted(
        error_counts.items(),
        key=lambda x: (-x[1], x[0]),
    )
    for code, count in sorted_errors:
        lines.append(f"{code}: {count}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def save_valid_only(data, path):
    """
    Keep only valid records in data and overwrite the file at path.
    Preserves generated_at; articles becomes only those that pass validate_record.
    """
    articles = data.get("articles", [])
    if not isinstance(articles, list):
        articles = []
    valid_articles = [r for r in articles if validate_record(r)[0]]
    out = {
        "generated_at": data.get("generated_at", ""),
        "articles": valid_articles,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(valid_articles)} valid records to {path}")


def main():
    input_path = "cleaned_output.json"
    output_path = "quality_report.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = validate(data)
    write_report(result, output_path)
    print("Generated quality_report.txt")

    save_valid_only(data, input_path)


if __name__ == "__main__":
    main()

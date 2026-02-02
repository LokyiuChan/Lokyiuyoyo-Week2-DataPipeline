# Prompt log

## Prompt: Data cleaning

I am building: Data Cleaning + Validation + Quality Report in Python.

Create a simple repo structure with these files:
- cleaner.py
- validator.py
- sample_data.json
- cleaned_output.json
- quality_report.txt
- README.md
- prompt-log.md

Add placeholder content to each file, but do NOT implement the full logic yet.

---

## Prompt: Data cleaning

Implement cleaner.py.

Requirements:
- Input: sample_data.json
- Output: cleaned_output.json (JSON array, same number of records, preserve records even if fields are missing; do not delete records here)

Cleaning functions:
1) Remove extra whitespace: strip and collapse internal whitespace to single spaces for title/content.
2) Remove HTML artifacts from title/content:
   - Remove tags like <p>, <br>, <h1>, etc.
   - Convert HTML entities like &nbsp; &amp; &quot; etc. to plain text.
3) Normalize text encoding:
   - Ensure output is valid UTF-8 in Python strings
   - Replace problematic invisible characters (e.g. non-breaking space) with normal spaces
4) Standardize date format:
   - Convert various input date formats into ISO
   - If date cannot be parsed, set date to "" (empty string) and keep the record
5) Handle special characters appropriately:
   - Keep meaningful characters (© ® ™) but remove control characters

Implementation details:
- Write modular functions (e.g., clean_text(), parse_date_to_iso()).
- Add a main guard so running `python3 cleaner.py` cleans the data.

---

## Prompt: Data validation and Quality report

Implement validator.py.
Requirements:
- Input: cleaned_output.json
- Output: quality_report.txt

Validation rules of input:
1) Required fields:
   - title, content, url must exist and must be non-empty after stripping whitespace.
2) URL format:
   - Must start with http:// or https://
3) Content length minimum:
   - content length must be >= 50 characters after stripping
4) For each invalid record, produce:
   - is_valid: true/false
   - errors: list of strings describing reasons (e.g., "missing_title", "missing_content", "missing_url", "invalid_url", "content_too_short"). Noted that a record can have multiple reasons.

Also compute field completeness counts:
- title_present_count
- content_present_count
- url_present_count
- date_present_count
Where "present" means the key exists and the stripped value is not empty.

Implementation details:
- Provide a function validate_record(record) -> (is_valid, errors)
- Validate all records and compute:
  - total_records
  - valid_count
  - invalid_count
  - completeness percentage per field
  - error_counts (frequency of each error reason code across all invalid records)
- Add a main guard so running `python3 validator.py` validates the cleaned data and writes quality_report.txt.

For the format of quality_report.txt:
======================
DATA QUALITY REPORT
======================
Total records processed: 
Valid records: 
Invalid records: 

----------------------
Completeness Summary
----------------------
Title completeness: title_percent%
Content completeness: content_percent%
URL completeness: url_percent%
Date completeness: date_percent%

----------------------
Common validation failures
----------------------
error 1: number
error2: number
...

Rules for report formatting:
- Percentages should be rounded to 2 decimal place.
- Show all reason codes that occurred, sorted by count descending.
- After writing the report, print a one-line confirmation: Generated quality_report.txt

---

## Prompt: README.md

Rewrite README.md to match the current project structure.

Current pipeline:
sample_data.json → cleaner.py → cleaned_output.json → validator.py → quality_report.txt

The project only uses:
- cleaner.py
- validator.py
- sample_data.json
- cleaned_output.json
- quality_report.txt

Write a concise, clear README.md (about 1 page) including:
1. Project overview
2. File structure
3. How to run (bullet points)
4. Validation rules (bullet points)


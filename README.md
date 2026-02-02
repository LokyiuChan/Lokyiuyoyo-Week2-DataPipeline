# Data Cleaning + Validation + Quality Report

## Project overview

This project cleans scraped article data and validates it, then produces a quality report. The pipeline is:

**sample_data.json** → **cleaner.py** → **cleaned_output.json** → **validator.py** → **quality_report.txt**

- **cleaner.py** reads `sample_data.json`, normalizes text (whitespace, HTML, encoding, dates), and writes `cleaned_output.json`.
- **validator.py** reads `cleaned_output.json`, checks each record against validation rules, and writes `quality_report.txt` with counts and error summaries.

## File structure

| File | Role |
|------|-----|
| `sample_data.json` | Input: JSON with `generated_at` and `articles` (url, title, content, published). |
| `cleaner.py` | Cleans input and writes cleaned JSON. |
| `cleaned_output.json` | Output of cleaner; input to validator. |
| `validator.py` | Validates cleaned data and writes the quality report. |
| `quality_report.txt` | Output: total/valid/invalid counts, completeness percentages, validation failure counts. |

## How to run

- Put your input data in `sample_data.json` (same structure as above).
- Optionally activate a virtual environment: `source venv/bin/activate`
- Run the cleaner:
  ```bash
  python3 cleaner.py
  ```
- Run the validator:
  ```bash
  python3 validator.py
  ```
- Inspect `cleaned_output.json` and `quality_report.txt`.

## Validation rules

The validator checks each article record and marks it valid only if all of the following hold:

- **Required fields:** `title`, `content`, and `url` must exist and be non-empty after stripping whitespace.
- **URL format:** `url` must start with `http://` or `https://`.
- **Content length:** `content` must have at least 50 characters after stripping.

Invalid records get one or more error codes: `missing_title`, `missing_content`, `missing_url`, `invalid_url`, `content_too_short`. 
The report also includes field completeness (title, content, url, date) as percentages and lists how often each error code occurred.

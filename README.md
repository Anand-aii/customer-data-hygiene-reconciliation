# Customer Data Hygiene & Reconciliation

A Python portfolio project demonstrating customer data cleaning, standardization, segmentation, suppression-list protection, and record reconciliation.

> **Portfolio demo:** All datasets are fictional and synthetically generated. This is not a real client project.

## Features

- Customer data cleaning and standardization
- Email validation and phone normalization
- Duplicate customer identification
- Four customer segment exports
- Suppression-list matching and exclusion
- Exact email and phone reconciliation
- Fuzzy name matching with RapidFuzz
- Unmatched record and manual review reports
- Automated validation checks

## Technology Stack

- Python 3
- Pandas
- OpenPyXL
- RapidFuzz
- Regular Expressions

## Demo Results

### Data Cleaning

| Metric | Result |
|---|---:|
| Input records | 515 |
| Duplicate records flagged | 15 |
| Quality passed | 467 |
| Records requiring review | 48 |

### Segmentation and Suppression

| Metric | Result |
|---|---:|
| Total records | 515 |
| Suppressed records | 10 |
| Exported records | 505 |
| Unmatched segment records | 0 |

### Customer Reconciliation

| Match category | Records |
|---|---:|
| Exact email matches | 10 |
| Exact phone matches | 10 |
| Possible fuzzy matches | 5 |
| Unmatched records | 5 |
| Manual review required | 10 |

### Validation

- Data validation: PASS
- Suppression validation: PASS
- Reconciliation validation: PASS

## Project Structure

- `src/` — Python source scripts
- `input/` — Generated synthetic input datasets
- `output/` — Cleaned Excel and segment exports
- `reports/` — Quality and reconciliation reports
- `requirements.txt` — Python dependencies

Input, output, and report data are generated locally and excluded from Git tracking.

## Installation

Clone the repository:

```bash
git clone https://github.com/Anand-aii/customer-data-hygiene-reconciliation.git
cd customer-data-hygiene-reconciliation
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Run these commands in order from the project directory:

```bash
python src/generate_data.py
python src/clean_data.py
python src/create_suppression.py
python src/export_segments.py
python src/validate_project.py
python src/create_reconciliation_data.py
python src/reconcile_customers.py
python src/validate_reconciliation.py
```

Generated Excel files, CSV exports, and reports are saved locally.

## Important Notes

- All data is fictional and generated for demonstration.
- Fuzzy matches are suggestions, not confirmed identities.
- Possible matches require manual review.
- Suppression matching currently uses normalized email addresses.
- This is a portfolio demonstration, not a production-ready integration system.

## About

Python customer data cleaning, segmentation, suppression, and reconciliation portfolio demo.

**GitHub:** https://github.com/Anand-aii

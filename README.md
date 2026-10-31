# Customer Data Hygiene & Reconciliation

## Project Overview

A Python-based portfolio demo for customer data cleaning, segmentation, suppression protection, and reconciliation.

**Note:** This project uses fictional synthetic data. It is not a real client project.

## Features

- Customer data cleaning and standardization
- Missing and invalid email detection
- Phone number normalization
- Duplicate customer identification
- Four customer segment exports
- Suppression-list matching and exclusion
- Exact email and phone matching
- Fuzzy name matching using RapidFuzz
- Unmatched customer reporting
- Automated validation reports

## Technology Stack

- Python 3
- Pandas
- OpenPyXL
- RapidFuzz
- Regular Expressions

## Demo Results

### Data Cleaning
- Input records: 515
- Duplicate records identified: 15
- Quality passed: 467
- Records requiring review: 48

### Segmentation and Suppression
- Total records: 515
- Suppressed records: 10
- Exported records: 505
- Unmatched segment records: 0

### Customer Reconciliation
- Source records: 30
- Exact email matches: 10
- Exact phone matches: 10
- Possible fuzzy matches: 5
- Unmatched records: 5
- Manual review required: 10

### Validation
- Data validation: PASS
- Suppression validation: PASS
- Reconciliation validation: PASS

## Project Structure

- `input/` — Synthetic input datasets
- `output/` — Cleaned Excel and segment exports
- `reports/` — Quality, suppression and matching reports
- `src/` — Python scripts
- `requirements.txt` — Python dependencies

## Installation

```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install -r requirements.txt
```

## Run the Project

Run these commands from the project directory:

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

## Important Notes

- All data is fictional and generated for demonstration.
- Fuzzy matches are possible matches, not confirmed identities.
- Possible matches require manual review.
- Suppression matching currently uses normalized email addresses.
- This is a portfolio demonstration, not a production-ready integration system.

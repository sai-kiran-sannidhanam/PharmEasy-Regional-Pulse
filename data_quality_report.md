# Data Quality Report: PharmEasy Regional Pulse Monthly Ingestion

This report evaluates the monthly order export against the 7 recognized dimensions of data quality and maps the cleaning operations executed in `clean_data.py`.

## Data Quality Dimensions & Applied Remediation

| Dimension | Definition | Pipeline Application / Fix Implemented | Status |
| :--- | :--- | :--- | :--- |
| **Uniqueness** | Records are free from duplicate entries and entities are represented exactly once. | **Task 1.2 Step 1:** Identified and removed 59 exact-duplicate rows across all 8 fields, reducing raw records from 2,159 to exactly 2,100 clean rows. | Resolved |
| **Consistency** | Data values across systems, tables, and representations adhere to uniform formats. | **Task 1.2 Step 2:** Stripped whitespace and applied title-casing to collapse 16 messy variants (e.g., `HYDERABAD `, `bengaluru `) into 9 canonical region names matching `regions_master.csv`. | Resolved |
| **Completeness** | All required operational attributes are populated without missing or null values. | **Task 1.2 Steps 3 & 4:** Imputed 48 missing category values via deterministic product mapping, and 94 missing profit values via category-level mean profit margins. | Resolved |
| **Validity** | Data conforms to defined business rules, domain schemas, and lookup constraints. | **Task 1.3:** Applied `validate_schema()` gate verifying all 8 mandatory columns are present with appropriate data types before downstream analytics. | Resolved |
| **Accuracy** | Data represents the real-world operational event without computational distortion. | Margin imputation used each category's observed mean margin ($profit\_inr / sales\_inr$) rather than an arbitrary global default, preserving product economics. | Resolved |
| **Timeliness** | Data is available within the active operational window and reflects the target period. | Verified all records fall strictly within Q1 FY26 (`2026-04-01` to `2026-06-30`), matching monthly reporting cadences. | Verified |
| **Relevance** | Ingested attributes directly answer regional performance and fulfillment questions. | Dataset retains order-level transactional dimensions required for desk-level MoM tracking, excluding unneeded system metadata. | Verified |

## Verification Checkpoint Summary
- **Raw Rows:** 2,159
- **Duplicates Removed:** 59 (Uniqueness addressed)
- **Canonical Regions Normalized:** 9 active regions (Consistency addressed)
- **Missing Categories Imputed:** 48 (Completeness addressed)
- **Missing Profit Imputed:** 94 (Completeness & Accuracy addressed)
- **Final Clean Rows:** 2,100
# PharmEasy Regional Pulse: Telugu & Bengaluru Desk

An end-to-end, SQL-verified, human-in-the-loop operational intelligence pipeline for PharmEasy's regional order monitoring.

---

## 4-Artifact Evaluation Cover Note

### 1. Headline Finding
Between April and May 2026, the Tier-2 cluster of **Guntur experienced an unprecedented +122.19% MoM sales surge** (from INR 39,268.04 to INR 87,249.49) backed by a 97.37% rise in distinct order volume, representing a permanent operational step-change that strains local warehouse fulfillment.

### 2. The 4 Deliverable Artifacts
- **Streamlit Interactive Dashboard (`app.py`):** Live exploration of headline KPIs, category wallet share, and regional time series with linked filtering.
- **Embedded CII Executive Summary (Top of `app.py`):** Concise 5-sentence operational summary framing what the data means before stakeholders drill into charts.
- **One-Page Recommendation Memo (`memo.md`):** Seven-field executive directive establishing concrete warehouse re-allocation and courier expansion in Guntur, with every factual claim risk-tiered.
- **Presentation Storyline (`presentation_storyline.md`):** Two-pronged audience-framed narrative (SCR for Executives, OCD for Regional Managers) with pushback defense using the Direct Acknowledgement Pattern.

### 3. Recommended Review Order
Reviewers should consume the artifacts in the following sequence:
1. **`memo.md`** — Read the 1-page executive recommendation and risk-tiered evidence.
2. **`app.py`** — Launch the dashboard to interactively stress-test the numbers and review the embedded CII summary.
3. **`presentation_storyline.md`** — Review the audience-tailored narrative and defense against pushback.
4. **`data_quality_report.md` & `reliability_checklist.md`** — Inspect data engineering lineage, validation gates, and audit logs.

### 4. Single Unverified Assumption Flagged Upfront
The demand acceleration in Guntur is assumed to stem from **newly onboarded clinic procurement networks and retail pharmacy aggregators**, rather than temporary consumer hoarding or competitor distribution failures (an assumption tagged `[MEDIUM]` risk in `memo.md`, to be verified via on-ground audits by July 5, 2026).

---

## Setup & End-to-End Execution Guide

Follow these exact steps from a clean clone to run the entire pipeline:

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
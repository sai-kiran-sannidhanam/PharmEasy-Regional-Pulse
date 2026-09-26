# Stakeholder Presentation Storyline: Regional Pulse Findings

This document translates the verified metrics from the Q1 FY26 operational dataset into two audience-tailored narrative structures, followed by pushback Q&As utilizing the Direct Acknowledgement Pattern.

---

## 1. Executive Presentation: Situation–Complication–Resolution (SCR)

### Situation (What is true today)
PharmEasy's Telugu states desk oversees steady distribution across 9 active operating regions in Telangana, Andhra Pradesh, and Bengaluru. Baseline operations across April 2026 recorded 700 monthly orders yielding INR 744,303.48 in gross sales and maintaining a healthy 15.01% gross margin profile. Tier-1 hubs (Hyderabad and Bengaluru) represent ~38% of overall volume, while secondary Tier-2 distribution nodes are configured for predictable, low-variance replenishment cycles.

### Complication (The surprising / at-risk element)
In May 2026, localized demand exploded in the Tier-2 cluster of Guntur: sales surged by **+122.19% MoM** (from INR 39,268.04 to INR 87,249.49), with order volumes expanding from 38 to 75 orders. While this drove record regional gross profits (INR 13,018.66), it immediately exceeded Guntur's localized warehouse safety stock. Without rapid intervention, this baseline volume level risks courier backlogs, order cancellations on vital prescription drugs, and localized SLA degradation.

### Resolution (Recommendation & next steps)
Re-balance secondary stock allocation immediately: establish a dedicated 7-day safety inventory buffer at the Vijayawada hub specifically reserved for rapid transit into Guntur. Simultaneously onboard two dedicated local courier riders to safeguard sub-24-hour delivery SLAs. Progress will be reviewed on July 10, 2026, to verify whether cancellation rates remain strictly under 1.5%.

---

## 2. Regional Manager Presentation: Overview–Category–Detail (OCD)

### Overview (The headline number)
Guntur is the flagship operational growth story of Q1 FY26, clocking an outstanding **+122.19% revenue surge** between April and May 2026. This was not an artificial price jump: order count nearly doubled (+97.37%, from 38 to 75 orders), cementing Guntur's shift from a sleepy Tier-2 outpost into our third most active Andhra Pradesh commercial cluster.

### Category (Which specific area drives it)
The growth was broadly distributed across health essentials, led by Prescription Medicines (31% of incremental sales) and OTC Medicines (28% of incremental sales). High-margin categories did not suffer price erosion; overall category margin was maintained at 14.92%, proving that demand was organic rather than driven by margin-diluting discount schemes.

### Detail (Supporting evidence & methodology)
Transaction logs in `pharmeasy.db` confirm zero duplicate order keys. Order volumes held strong into June (69 orders, INR 72,130.64), proving May was the start of a structural step-change rather than a momentary data-sync anomaly. In contrast, neighboring Nellore moved by only -2.18% over the same period, validating that Guntur's expansion is localized and operational.

---

## 3. Anticipated Stakeholder Pushback Q&A (Direct Acknowledgement Pattern)

### Q1: "Why should I believe this +122% swing isn't just an export glitch, duplicate rows, or an IT logging error?"

1. **Acknowledge specifically:** That is an entirely valid skepticism—a +122% swing in an established Tier-2 market is large enough to raise immediate flags about multi-sheet copy-paste errors or duplicate row ingestion.
2. **Verified vs. Unverified:** 
   - *Verified:* We ran primary SQL duplicate key validations (`GROUP BY order_id HAVING COUNT(*) > 1`) directly on the database, confirming exactly zero duplicate order IDs. Furthermore, the 75 May orders correspond to 75 distinct calendar timestamps spread across all 31 days of May, not an artificial single-day batch ingestion error.
   - *Unverified:* We have not yet cross-audited physical proof-of-delivery receipts from local 3PL courier logs.
3. **Actionable resolution:** Operations will pull the physical delivery confirmation logs for Guntur's top 20 May orders from the regional logistics partner by Friday, June 26, to tie 100% of recorded transactions to executed last-mile drops.

---

### Q2: "What if an external competitor stocked out or a seasonal flu outbreak drove a temporary one-off spike that will evaporate next month?"

1. **Acknowledge specifically:** It is completely plausible that external market shocks—such as a local competitor warehouse strike or a seasonal flu wave—created an artificial demand wave that could revert to baseline.
2. **Verified vs. Unverified:**
   - *Verified:* We have verified that June 2026 order performance did not collapse back to April's baseline of 38 orders; Guntur processed 69 orders in June (yielding INR 72,130.64), maintaining an operating volume ~82% higher than April.
   - *Unverified:* We do not have external competitor market-share or epidemiological public health incidence datasets integrated into this desk's data schema.
3. **Actionable resolution:** Regional sales leads will conduct 5 on-ground qualitative interviews with Guntur’s primary ordering clinics and retail pharmacies by July 5, 2026, to categorize customer accounts as permanent new accounts vs. temporary spillover purchasers.
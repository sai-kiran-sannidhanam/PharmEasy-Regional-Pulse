# Reliability Checklist: PharmEasy Regional Pulse

This 4-step checklist must be completed and signed before any automated insight or analytical memo is marked `approved` for executive review.

1. **Safety Check:** Verified that all customer personal identifying information (PII), patient contact numbers, prescription images, and exact delivery addresses are completely absent from the reporting pipeline, restricting all shared outputs exclusively to regional aggregates.
2. **Validation:** Confirmed that every numerical claim in the narrative memo and dashboard matches byte-for-byte with the output of the local SQLite metrics engine (`pharmeasy.db`), with duplicate-free order keys and verified relational joins.
3. **Critique / Refine:** Filtered out ungrounded external hypotheses regarding competitor campaigns or festival spikes, ensuring any unverified operational assumptions are explicitly segregated into the assumptions field and assigned an inline verification risk tier.
4. **Human Sign-Off:** The Telugu regional operations desk lead manually reviewed the draft report and confirmed that the Guntur surge is an operational signal requiring warehouse replenishment intervention rather than an ingest artifact.
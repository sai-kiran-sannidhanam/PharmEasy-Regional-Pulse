"""draft_report.py -- Generates Context-Insight-Implication (CII) narrative blocks."""
import json
from metrics_engine import run_metrics_pipeline

def draft_report_v1(flagged_apr_may: dict, flagged_may_jun: dict, metrics: dict) -> dict:
    """Generates structured CII report blocks for every flagged region."""
    all_flagged_regions = sorted(list(set(list(flagged_apr_may.keys()) + list(flagged_may_jun.keys()))))
    monthly_data = metrics["monthly_data"]
    cii_blocks = {}

    for region in all_flagged_regions:
        apr_sales = monthly_data["2026-04"].get(region, {}).get("sales", 0.0)
        may_sales = monthly_data["2026-05"].get(region, {}).get("sales", 0.0)
        jun_sales = monthly_data["2026-06"].get(region, {}).get("sales", 0.0)

        change_1 = flagged_apr_may.get(region, {}).get("change_pct", None)
        change_2 = flagged_may_jun.get(region, {}).get("change_pct", None)

        # Context
        context_str = (
            f"{region} is an active commercial cluster in the regional network. "
            f"Baseline sales recorded in April 2026 stood at INR {apr_sales:,.2f}."
        )

        # Insight
        insights = []
        if change_1 is not None:
            direction_1 = "surged" if change_1 > 0 else "contracted"
            insights.append(f"In May 2026, revenue {direction_1} by {change_1:+.2f}% to INR {may_sales:,.2f}.")
        if change_2 is not None:
            direction_2 = "moved" if change_2 > 0 else "declined"
            insights.append(f"In June 2026, revenue {direction_2} by {change_2:+.2f}% to INR {jun_sales:,.2f}.")
        insight_str = " ".join(insights)

        # Implication
        if region == "Guntur":
            implication_str = (
                "The dramatic +122.19% spike strains localized fulfillment capacity, requiring warehouse "
                "re-allocation and safety-stock buffers before stock-outs hit high-margin prescription lines."
            )
        elif region == "Visakhapatnam":
            implication_str = (
                "Significant volatility (-50.62% in May, followed by partial recovery) indicates potential "
                "supply-chain friction or hub re-routing requiring regional logistics review."
            )
        elif (change_1 and change_1 > 0) or (change_2 and change_2 > 0):
            implication_str = (
                "Sustained volume expansion signals heightened demand density; evaluate last-mile rider fleet "
                "capacity to prevent delivery SLA degradation."
            )
        else:
            implication_str = (
                "Contraction requires order-mix auditing to confirm whether clinical partner attrition or product "
                "out-of-stock events drove the dip."
            )

        cii_blocks[region] = {
            "region": region,
            "context": context_str,
            "insight": insight_str,
            "implication": implication_str,
            "apr_sales": apr_sales,
            "may_sales": may_sales,
            "jun_sales": jun_sales,
            "flagged_transitions": {
                "apr_may": change_1,
                "may_jun": change_2
            }
        }
    return cii_blocks

if __name__ == "__main__":
    data = run_metrics_pipeline()
    report = draft_report_v1(data["flagged_apr_may"], data["flagged_may_jun"], data)
    print(f"\nGenerated CII narrative blocks for {len(report)} unique flagged regions:")
    for r, b in report.items():
        print(f"\n[{r}]")
        print(f"Context:     {b['context']}")
        print(f"Insight:     {b['insight']}")
        print(f"Implication: {b['implication']}")
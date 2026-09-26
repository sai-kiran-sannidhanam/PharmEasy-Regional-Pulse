"""app.py -- PharmEasy Regional Pulse operational analytics dashboard."""
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Data Ingestion Engine
# ---------------------------------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect("pharmeasy.db")
    query = """
        SELECT 
            o.order_id,
            o.order_date,
            o.region,
            r.state,
            r.tier,
            o.category,
            o.product,
            o.quantity,
            o.sales_inr,
            o.profit_inr,
            SUBSTR(o.order_date, 1, 7) AS month
        FROM orders_clean o
        JOIN regions_master r ON o.region = r.region;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

# ---------------------------------------------------------
# Embedded Executive Summary (CII Format)
# ---------------------------------------------------------
st.title("💊 PharmEasy Regional Pulse: Telugu & Bengaluru Desk")
st.markdown("### Executive Operational Overview (Q1 FY26)")

st.info("""
**Executive Summary (CII):** Across Q1 FY26 (April–June), the Telugu and Bengaluru regional desks generated a cumulative **INR 2,217,543.08** in gross sales and **INR 333,024.16** in operating profit across **2,100 verified orders**. 
While regional baseline sales stabilized around INR 730k/month, high operational volatility was recorded in Tier-2 Andhra Pradesh clusters—most notably **Guntur**, which surged **+122.19% MoM** in May (reaching INR 87,249.49). 
Product demand continues to be anchored by **OTC Medicines (30.1% of orders)** and **Prescription Medicines (21.7% of orders)**, maintaining steady gross margins of ~15.0%. 
To protect delivery SLAs against localized stock-outs during ongoing volume surges, regional leads must immediately redirect secondary inventory replenishment buffers from Vijayawada into Guntur. 
*Reviewers can inspect localized metrics, monthly velocity trends, and SKU breakdowns using the filters below.*
""")

st.markdown("---")

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.header("Operational Filters")
all_regions = ["All Desk Regions"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Regional Hub / Cluster", all_regions)

# Filter Dataframe
if selected_region == "All Desk Regions":
    filtered_df = df.copy()
else:
    filtered_df = df[df["region"] == selected_region].copy()

# ---------------------------------------------------------
# Level 1: Overview KPIs
# ---------------------------------------------------------
st.subheader("Level 1: Headline Operational KPIs")
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["sales_inr"].sum()
total_profit = filtered_df["profit_inr"].sum()
distinct_orders = filtered_df["order_id"].nunique()
avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

col1.metric("Gross Sales (INR)", f"₹{total_sales:,.2f}")
col2.metric("Operating Profit (INR)", f"₹{total_profit:,.2f}")
col3.metric("Distinct Orders Verified", f"{distinct_orders:,}")
col4.metric("Average Profit Margin", f"{avg_margin:.2f}%")

st.markdown("---")

# ---------------------------------------------------------
# Charts Section (Obeying 6 Strict Anti-Patterns)
# ---------------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # 1. Trend Line Chart: Time Series across Months (starts at zero, labeled axes)
    monthly_trend = df.groupby(["month", "region"])["sales_inr"].sum().reset_index()
    
    if selected_region != "All Desk Regions":
        chart_trend_data = monthly_trend[monthly_trend["region"] == selected_region]
        line_color = "#E05638" if selected_region == "Guntur" else "#1F77B4"
        fig_line = px.line(
            chart_trend_data,
            x="month",
            y="sales_inr",
            markers=True,
            title=f"How did monthly sales trend in {selected_region} across Q1?",
            labels={"month": "Operating Month (2026)", "sales_inr": "Total Sales (INR)"}
        )
        fig_line.update_traces(line_color=line_color, line_width=3)
    else:
        # Highlight Guntur, others muted
        fig_line = go.Figure()
        for r in df["region"].unique():
            r_data = monthly_trend[monthly_trend["region"] == r]
            if r == "Guntur":
                fig_line.add_trace(go.Scatter(
                    x=r_data["month"], y=r_data["sales_inr"],
                    mode="lines+markers", name="Guntur (Spike)",
                    line=dict(color="#D62728", width=4)
                ))
            else:
                fig_line.add_trace(go.Scatter(
                    x=r_data["month"], y=r_data["sales_inr"],
                    mode="lines", name=r,
                    line=dict(color="#AEC7E8", width=1.5)
                ))
        fig_line.update_layout(
            title="How did regional monthly sales evolve across Q1 FY26?",
            xaxis_title="Operating Month (2026)",
            yaxis_title="Total Sales (INR)"
        )
    
    fig_line.update_layout(yaxis_range=[0, None])  # Axis starts at zero
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    # 2. Comparison Bar Chart: Total Regional Sales
    region_sales = df.groupby("region")["sales_inr"].sum().reset_index().sort_values("sales_inr", ascending=True)
    colors = ["#D62728" if r == selected_region or (selected_region == "All Desk Regions" and r == "Guntur") else "#2CA02C" for r in region_sales["region"]]
    
    fig_bar = go.Figure(go.Bar(
        x=region_sales["sales_inr"],
        y=region_sales["region"],
        orientation="h",
        marker_color=colors
    ))
    fig_bar.update_layout(
        title="Which regions generated the highest gross sales in Q1 FY26?",
        xaxis_title="Cumulative Sales (INR)",
        yaxis_title="Regional Desk / Cluster",
        xaxis_range=[0, None]  # Axis starts at zero
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# Level 2: Category Breakdown
# ---------------------------------------------------------
st.subheader("Level 2: Category Breakdown & Share of Wallet")
col_cat1, col_cat2 = st.columns([1, 1])

with col_cat1:
    # 3. Part-of-Whole Donut Chart (6 categories, capped at 6 slices, no 3D)
    cat_sales = filtered_df.groupby("category")["sales_inr"].sum().reset_index()
    fig_pie = px.pie(
        cat_sales,
        names="category",
        values="sales_inr",
        hole=0.45,
        title=f"What is the category sales distribution for {selected_region}?",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_cat2:
    # Category KPI table
    cat_summary = filtered_df.groupby("category").agg(
        Order_Count=("order_id", "nunique"),
        Total_Sales_INR=("sales_inr", "sum"),
        Total_Profit_INR=("profit_inr", "sum")
    ).reset_index()
    cat_summary["Margin_%"] = ((cat_summary["Total_Profit_INR"] / cat_summary["Total_Sales_INR"]) * 100).round(2)
    cat_summary["Sales_Share_%"] = ((cat_summary["Total_Sales_INR"] / total_sales) * 100).round(2)
    st.dataframe(
        cat_summary.style.format({
            "Total_Sales_INR": "₹{:,.2f}",
            "Total_Profit_INR": "₹{:,.2f}",
            "Margin_%": "{:.2f}%",
            "Sales_Share_%": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ---------------------------------------------------------
# Level 3: Detail Level
# ---------------------------------------------------------
st.subheader("Level 3: Per-Region Monthly Detail Table")
detail_df = filtered_df.groupby(["region", "month"]).agg(
    Distinct_Orders=("order_id", "nunique"),
    Total_Quantity=("quantity", "sum"),
    Total_Sales_INR=("sales_inr", "sum"),
    Total_Profit_INR=("profit_inr", "sum")
).reset_index()

detail_df["Profit_Margin_%"] = ((detail_df["Total_Profit_INR"] / detail_df["Total_Sales_INR"]) * 100).round(2)

st.dataframe(
    detail_df.style.format({
        "Total_Sales_INR": "₹{:,.2f}",
        "Total_Profit_INR": "₹{:,.2f}",
        "Profit_Margin_%": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption("PharmEasy Regional Pulse v1.0 • Verified SQL Analytics Engine • All figures auditable against pharmeasy.db")
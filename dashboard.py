# =====================================================
# 🚗 CAR SALES ADVANCED DASHBOARD
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Car Sales Intelligence Dashboard",
    page_icon="🚗",
    layout="wide"
)

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🚗 Car Sales Intelligence Dashboard</h1>
    <p style='text-align: center; font-size:18px;'>
    Advanced analytical dashboard for strategic decision-making
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
import gdown

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1566PtRghmt7j07ekSqXTyjdpPVRGFDBy"
    gdown.download(url, "car_sales.csv", quiet=False)
    df = pd.read_csv("car_sales.csv", encoding="latin-1")
    return df

df = load_data()


# -----------------------------------------------------
# DATA PREPARATION
# -----------------------------------------------------
df['Date'] = pd.to_datetime(df['Date'])
df['Revenue'] = df['Sale Price'] * df['Quantity']
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter


# -----------------------------------------------------
# SIDEBAR – FILTERS
# -----------------------------------------------------
st.sidebar.title("🎛️ Dashboard Filters")

year_filter = st.sidebar.multiselect(
    "📅 Select Year(s)",
    sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

region_filter = st.sidebar.multiselect(
    "🌍 Select Region(s)",
    sorted(df['Sales Region'].unique()),
    default=sorted(df['Sales Region'].unique())
)

top_n = st.sidebar.slider(
    "🔢 Select Top N",
    min_value=1,
    max_value=20,
    value=10
)

df_filt = df[
    (df['Year'].isin(year_filter)) &
    (df['Sales Region'].isin(region_filter))
]

# -----------------------------------------------------
# KPI SECTION
# -----------------------------------------------------
st.markdown("## 📊 Global Key Performance Indicators")
st.caption("High-level metrics summarizing overall business performance.")

total_revenue = df_filt['Revenue'].sum()
total_quantity = df_filt['Quantity'].sum()
num_customers = df_filt['Customer Name'].nunique()
num_orders = len(df_filt)
avg_basket = total_revenue / num_orders

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Revenue", f"${total_revenue/1e9:.2f} B")
c2.metric("📦 Quantity", f"{total_quantity:,}")
c3.metric("👥 Customers", f"{num_customers:,}")
c4.metric("🧾 Orders", f"{num_orders:,}")
c5.metric("🛒 Avg Basket", f"${avg_basket:,.0f}")

# -----------------------------------------------------
# SALES EVOLUTION
# -----------------------------------------------------
st.markdown("## 📈 Sales Evolution Over Time")
st.caption(
    "This chart shows how revenue evolves monthly. "
    "It helps identify trends, growth phases, and seasonal patterns."
)

monthly_sales = (
    df_filt.groupby(['Year', 'Month'])['Revenue']
    .sum()
    .reset_index()
)

fig_time = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    color="Year",
    markers=True,
    template="plotly_white"
)
st.plotly_chart(fig_time, use_container_width=True)

# -----------------------------------------------------
# SEASONALITY
# -----------------------------------------------------
st.markdown("## 🗓️ Seasonality Analysis")
st.caption(
    "Quarterly aggregation highlights recurring seasonal effects "
    "in vehicle purchases."
)

quarter_sales = (
    df_filt.groupby('Quarter')['Revenue']
    .sum()
    .reset_index()
)

fig_quarter = px.bar(
    quarter_sales,
    x="Quarter",
    y="Revenue",
    color="Quarter",
    template="plotly_white"
)
st.plotly_chart(fig_quarter, use_container_width=True)

# -----------------------------------------------------
# COVID IMPACT
# -----------------------------------------------------
st.markdown("## 🦠 COVID-19 Impact on Car Sales")
st.caption(
    "Comparison of monthly revenue before, during, and after COVID-19. "
    "The drop in 2020 reflects lockdowns and economic uncertainty."
)

covid_df = df[df['Year'].isin([2019, 2020, 2021])]
covid_monthly = (
    covid_df.groupby(['Year', 'Month'])['Revenue']
    .sum()
    .reset_index()
)

fig_covid = px.line(
    covid_monthly,
    x="Month",
    y="Revenue",
    color="Year",
    markers=True,
    template="plotly_white"
)
st.plotly_chart(fig_covid, use_container_width=True)

# -----------------------------------------------------
# PRODUCT PERFORMANCE
# -----------------------------------------------------
st.markdown("## 🚗 Product Performance")
st.caption(
    "Top and weak-performing car brands based on revenue and quantity sold."
)

product_perf = (
    df_filt.groupby('Car Make')
    .agg(Revenue=('Revenue', 'sum'), Quantity=('Quantity', 'sum'))
    .reset_index()
)

top_products = product_perf.sort_values("Revenue", ascending=False).head(top_n)
flop_products = product_perf.sort_values("Revenue").head(top_n)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### ⭐ Top {top_n} Products")
    st.dataframe(top_products)

with col2:
    st.markdown(f"### ⚠️ Bottom {top_n} Products")
    st.dataframe(flop_products)

# -----------------------------------------------------
# CUSTOMER VALUE – PARETO
# -----------------------------------------------------
st.markdown("## 👑 Customer Value (Pareto 80/20)")
st.caption(
    "This curve shows that a small percentage of customers "
    "generate most of the revenue."
)

customer_rev = (
    df_filt.groupby('Customer Name')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

customer_rev['Cumulative %'] = customer_rev['Revenue'].cumsum() / customer_rev['Revenue'].sum()

fig_pareto = px.line(
    customer_rev,
    y="Cumulative %",
    template="plotly_white"
)
st.plotly_chart(fig_pareto, use_container_width=True)

# -----------------------------------------------------
# CUSTOMER LOYALTY
# -----------------------------------------------------
st.markdown("## 🔁 Customer Loyalty")
st.caption(
    "Customers with repeated purchases represent long-term value "
    "and should be prioritized."
)

repeat_customers = (
    df_filt.groupby('Customer Name')
    .size()
    .reset_index(name="Number of Purchases")
    .sort_values("Number of Purchases", ascending=False)
    .head(top_n)
)

st.dataframe(repeat_customers)

# -----------------------------------------------------
# SELLER PERFORMANCE
# -----------------------------------------------------
st.markdown("## 🧑‍💼 Seller Performance")
st.caption(
    "Identifies top salespeople generating the highest revenue."
)

seller_perf = (
    df_filt.groupby('Salesperson')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)

fig_sellers = px.bar(
    seller_perf,
    x="Salesperson",
    y="Revenue",
    color="Revenue",
    template="plotly_white"
)
st.plotly_chart(fig_sellers, use_container_width=True)

# -----------------------------------------------------
# REGIONAL STABILITY
# -----------------------------------------------------
st.markdown("## 🌍 Regional Stability Analysis")
st.caption(
    "Regions with high revenue volatility are considered irregular, "
    "while low volatility indicates stable markets."
)

region_volatility = (
    df.groupby('Sales Region')['Revenue']
    .std()
    .reset_index(name="Revenue Volatility")
    .sort_values("Revenue Volatility")
)

st.dataframe(region_volatility)
#agepreference
st.markdown("---")
st.header("🚗 Car Preferences by Age Group")

st.markdown("""
This section analyzes **which types of cars are most frequently purchased
by different age groups**, helping understand generational preferences.
""")

# Correct Age Group
df['Age Group'] = pd.cut(
    df['Customer Age'],  # <--- ici on prend "Customer Age"
    bins=[18, 25, 35, 45, 55, 65, 100],
    labels=['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
)

# Aggregate purchases by Age Group and Car Make (or Car Model)
age_car_pref = (
    df.groupby(['Age Group', 'Car Make'])  # <--- ici "Car Make" ou "Car Model"
    .size()
    .reset_index(name='Purchases')
)

# Interactive selector
selected_age = st.selectbox(
    "Select Age Group",
    age_car_pref['Age Group'].unique()
)

filtered_age_pref = age_car_pref[age_car_pref['Age Group'] == selected_age]

fig_age = px.bar(
    filtered_age_pref.sort_values('Purchases', ascending=False),
    x='Car Make',  # <--- colonne correcte
    y='Purchases',
    title=f"Most Purchased Cars – Age Group {selected_age}",
    labels={'Purchases': 'Number of Purchases', 'Car Make': 'Car Make'}
)

st.plotly_chart(fig_age, use_container_width=True)

st.info(
    "🔎 **Interpretation:** This chart highlights how car preferences vary by age. "
    "Younger customers tend to prefer modern and compact cars, while older age groups "
    "show interest in comfort and reliability-focused models."
)

#RFM ANALYSIS
st.markdown("---")
st.header("📊 RFM Customer Segmentation")

st.markdown("""
RFM analysis segments customers based on:
- **Recency**: How recently they purchased
- **Frequency**: How often they purchased
- **Monetary**: How much they spent
""")

# Create Sale Date from Year and Month
df['Sale Date'] = pd.to_datetime(
    df["Sale Year"].astype(str) + "-" +
    df["Sale Month"].astype(str) + "-01"
)

# Reference date (one day after the last sale)
reference_date = df['Sale Date'].max() + pd.Timedelta(days=1)

# RFM table using Customer Name
rfm = df.groupby('Customer Name').agg({
    'Sale Date': lambda x: (reference_date - x.max()).days,  # Recency
    'Quantity': 'count',  # Frequency
    'Revenue': 'sum'      # Monetary
}).reset_index()

rfm.columns = ['Customer Name', 'Recency', 'Frequency', 'Monetary']

# Determine number of bins for Recency, Frequency, Monetary
def qcut_safe(series, q=4, ascending=True):
    # Drop duplicates in bins
    bins = pd.qcut(series, q, duplicates='drop')
    # Determine actual number of bins
    n_bins = bins.cat.categories.size
    # Generate labels dynamically
    if ascending:
        labels = list(range(n_bins, 0, -1))  # High recency = low score
    else:
        labels = list(range(1, n_bins+1))    # High value = high score
    # Apply qcut again with correct labels
    return pd.qcut(series, q, labels=labels, duplicates='drop')

# Apply to RFM
rfm['R_Score'] = qcut_safe(rfm['Recency'], q=4, ascending=True)   # Lower recency = higher score
rfm['F_Score'] = qcut_safe(rfm['Frequency'], q=4, ascending=False) # Higher frequency = higher score
rfm['M_Score'] = qcut_safe(rfm['Monetary'], q=4, ascending=False)  # Higher monetary = higher score



# Combine RFM score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Segment definition
def segment_customer(row):
    if row['RFM_Score'] >= '444':
        return 'Champions'
    elif row['RFM_Score'] >= '344':
        return 'Loyal Customers'
    elif row['RFM_Score'] >= '244':
        return 'Potential Loyalists'
    elif row['RFM_Score'] >= '144':
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Count customers per segment
segment_count = rfm['Segment'].value_counts().reset_index()
segment_count.columns = ['Segment', 'Customers']

# Pie chart for segments
fig_rfm = px.pie(
    segment_count,
    names='Segment',
    values='Customers',
    title='Customer Segmentation using RFM Analysis',
    hole=0.4
)

st.plotly_chart(fig_rfm, use_container_width=True)

st.success(
    "💡 **Business Insight:** RFM segmentation helps identify high-value customers "
    "to target with loyalty programs and detect customers at risk of churn."
)


# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
st.markdown("---")
st.markdown(
    "📌 **Built with Python, Pandas, Plotly & Streamlit — Data-Driven Decision Dashboard**"
)

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Factory-to-Customer Shipping Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

h1{
    color:#0F172A;
    font-weight:700;
}

h2,h3{
    color:#1E3A8A;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:12px;
    padding:18px;
    border:1px solid #E5E7EB;
    box-shadow:0 3px 8px rgba(0,0,0,.08);
}

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

hr{
    margin-top:5px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_data.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    return df


df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("🚚 Dashboard Filters")

# Date
date_range = st.sidebar.date_input(
    "📅 Order Date",
    [
        df["Order Date"].min(),
        df["Order Date"].max()
    ]
)

# Region
regions = sorted(df["Region"].dropna().unique())

selected_region = st.sidebar.multiselect(
    "🌍 Region",
    regions,
    default=regions
)

# State
states = sorted(df["State/Province"].dropna().unique())

selected_state = st.sidebar.multiselect(
    "📍 State",
    states,
    default=states
)

# Factory
factories = sorted(df["Factory"].dropna().unique())

selected_factory = st.sidebar.multiselect(
    "🏭 Factory",
    factories,
    default=factories
)

# Ship Mode
ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_ship = st.sidebar.multiselect(
    "🚚 Ship Mode",
    ship_modes,
    default=ship_modes
)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# ==========================================================
# APPLY FILTERS
# ==========================================================
filtered_df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(selected_region)) &
    (df["State/Province"].isin(selected_state)) &
    (df["Factory"].isin(selected_factory)) &
    (df["Ship Mode"].isin(selected_ship))
]

# ==========================================================
# HEADER
# ==========================================================
st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

st.markdown("""
Analyze factory performance, shipping routes,
customer locations and business performance through
interactive visualizations.
""")

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💰 Total Sales",
        f"${filtered_df['Sales'].sum():,.0f}"
    )

with k2:
    st.metric(
        "📦 Orders",
        filtered_df["Order ID"].nunique()
    )

with k3:
    st.metric(
        "💵 Gross Profit",
        f"${filtered_df['Gross Profit'].sum():,.0f}"
    )

with k4:
    st.metric(
        "🚚 Avg Shipping Days",
        round(filtered_df["Shipping Days"].mean(),2)
    )

st.divider()

# ==========================================================
# DASHBOARD LAYOUT (EMPTY PLACEHOLDERS)
# ==========================================================

# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("📊 Sales by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=True)
    )

    fig_region = px.bar(
        region_sales,
        x="Sales",
        y="Region",
        orientation="h",
        color="Sales",
        template="plotly_white"
    )

    st.plotly_chart(fig_region, use_container_width=True)
    
    #.   col2 ---
with col2:
    st.subheader("🗺️ Sales Distribution by State")

    state_analysis = (
        filtered_df.groupby("State/Province")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Orders=("Order ID", "count")
        )
        .reset_index()
    )

    fig_map = px.choropleth(
        state_analysis,
        locations="State/Province",
        locationmode="USA-states",
        color="Total_Sales",
        hover_data=["Total_Orders"],
        scope="usa",
        color_continuous_scale="Blues",
        title="Sales by State"
    )

    fig_map.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(fig_map, use_container_width=True)
    
    #-col 3--------
with col3:
    st.subheader("📈 Monthly Sales Trend")

    # Create Month Column
    filtered_df["Order Month"] = (
        filtered_df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Monthly Sales
    monthly_sales = (
        filtered_df.groupby("Order Month")
        .agg(
            Total_Sales=("Sales", "sum")
        )
        .reset_index()
    )

    # Line Chart
    fig_month = px.line(
        monthly_sales,
        x="Order Month",
        y="Total_Sales",
        markers=True,
        title="Monthly Sales Trend",
        template="plotly_white"
    )

    fig_month.update_traces(
        line_color="#2563EB",
        line_width=3,
        marker_size=8
    )

    fig_month.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Month",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(fig_month, use_container_width=True)

st.divider()

# Row 2
col4, col5, col6 = st.columns(3)
# row 2--- col 1
with col4:

    st.subheader("🛣️ Route Performance")

    route_analysis = (
        filtered_df.groupby("Route", as_index=False)
        .agg(
            Total_Orders=("Order ID", "count"),
            Total_Sales=("Sales", "sum"),
            Avg_Shipping_Days=("Shipping Days", "mean")
        )
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    fig_route = px.bar(
        route_analysis,
        x="Total_Sales",
        y="Route",
        orientation="h",
        color="Avg_Shipping_Days",   # ✅ Same color scale as before
        text="Total_Sales",
        template="plotly_white",
        color_continuous_scale="Blues"
    )

    # Sirf ye line add karo
    fig_route.update_yaxes(autorange="reversed")

    fig_route.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    fig_route.update_layout(
        title="Top 10 Routes by Sales",
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Sales ($)",
        yaxis_title=""
    )

    st.plotly_chart(fig_route, use_container_width=True)    
    #-- row 2--col2-- 
with col5:
    st.subheader("🏭 Factory Performance")

    factory_analysis = (
        filtered_df.groupby("Factory")
        .agg(
            Total_Orders=("Order ID", "count"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Avg_Shipping_Days=("Shipping Days", "mean")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

    fig_factory = px.bar(
        factory_analysis,
        x="Factory",
        y="Total_Sales",
        color="Total_Profit",
        text_auto=".2s",
        title="Factory-wise Sales Performance",
        template="plotly_white",
        color_continuous_scale="Greens"
    )

    fig_factory.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Factory",
        yaxis_title="Sales ($)",
        xaxis_tickangle=-30
    )

    fig_factory.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig_factory, use_container_width=True)
    
    #row 2 -- col3 
with col6:
    st.subheader("🚚 Shipping Mode Performance")

    shipping_mode = (
        filtered_df.groupby("Ship Mode")
        .agg(
            Total_Orders=("Order ID", "count"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Avg_Shipping_Days=("Shipping Days", "mean")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

    fig_mode = px.bar(
        shipping_mode,
        x="Ship Mode",
        y="Total_Sales",
        color="Avg_Shipping_Days",
        text="Total_Sales",
        hover_data=["Total_Orders", "Total_Profit"],
        title="Shipping Mode Performance",
        template="plotly_white",
        color_continuous_scale="Oranges"
    )

    fig_mode.update_traces(
        texttemplate="$%{text:.2s}",
        textposition="outside"
    )

    fig_mode.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Shipping Mode",
        yaxis_title="Sales ($)",
        xaxis_tickangle=-20,
        showlegend=False
    )

    st.plotly_chart(fig_mode, use_container_width=True)
   

st.divider()

# Row 3
col7, col8, col9 = st.columns(3)
 # row 3 --- col 1
with col7:
    st.subheader("📦 Top 10 Products")

    product_analysis = (
        filtered_df.groupby("Product Name")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Total_Units=("Units", "sum")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    fig_product = px.bar(
        product_analysis,
        x="Total_Sales",
        y="Product Name",
        orientation="h",
        color="Total_Profit",
        text="Total_Units",
        title="Top 10 Products by Sales",
        template="plotly_white",
        color_continuous_scale="Viridis"
    )

    fig_product.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    fig_product.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Sales ($)",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig_product, use_container_width=True)
    
    #row 3-- col 2
with col8:
    st.subheader("📈 Monthly Gross Profit Trend")

    # Create Month Column
    filtered_df["Order Month"] = (
        filtered_df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Monthly Profit
    monthly_profit = (
        filtered_df.groupby("Order Month")
        .agg(
            Total_Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    # Line Chart
    fig_profit = px.line(
        monthly_profit,
        x="Order Month",
        y="Total_Profit",
        markers=True,
        title="Monthly Gross Profit",
        template="plotly_white"
    )

    fig_profit.update_traces(
        line=dict(color="#16A34A", width=3),
        marker=dict(size=8)
    )

    fig_profit.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Month",
        yaxis_title="Gross Profit ($)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_profit, use_container_width=True)
    # row 3 - col 3
with col9:
    st.subheader("🌎 Top 10 States by Sales")

    state_analysis = (
        filtered_df.groupby("State/Province")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Orders=("Order ID", "count"),
            Total_Profit=("Gross Profit", "sum")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    fig_state = px.bar(
        state_analysis,
        x="Total_Sales",
        y="State/Province",
        orientation="h",
        color="Total_Profit",
        text="Total_Sales",
        title="Top 10 States by Sales",
        template="plotly_white",
        color_continuous_scale="Blues"
    )

    fig_state.update_traces(
        texttemplate="$%{text:.2s}",
        textposition="outside"
    )

    fig_state.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Sales ($)",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    st.plotly_chart(fig_state, use_container_width=True)

st.divider()

# Row 4
col10, col11, col12 = st.columns(3)
# row 4 - col 1--
with col10:
    st.subheader("🏙️ Top Customer Cities")

    city_analysis = (
        filtered_df.groupby("City")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Orders=("Order ID", "count"),
            Total_Profit=("Gross Profit", "sum")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    fig_city = px.bar(
        city_analysis,
        x="Total_Sales",
        y="City",
        orientation="h",
        color="Total_Orders",
        text="Total_Sales",
        title="Top 10 Cities by Sales",
        template="plotly_white",
        color_continuous_scale="Teal"
    )

    fig_city.update_traces(
        texttemplate="$%{text:.2s}",
        textposition="outside"
    )

    fig_city.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Sales ($)",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    st.plotly_chart(fig_city, use_container_width=True)
    # row 4- col 2------
with col11:
    st.subheader("👥 Top 10 Customers")

    customer_analysis = (
        filtered_df.groupby("Customer ID")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Orders=("Order ID", "count"),
            Total_Profit=("Gross Profit", "sum")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    fig_customer = px.bar(
        customer_analysis,
        x="Total_Sales",
        y="Customer ID",
        orientation="h",
        color="Total_Profit",
        text="Total_Sales",
        title="Top 10 Customers by Sales",
        template="plotly_white",
        color_continuous_scale="Purples"
    )

    fig_customer.update_traces(
        texttemplate="$%{text:.2s}",
        textposition="outside"
    )

    fig_customer.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Sales ($)",
        yaxis_title="Customer ID",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    st.plotly_chart(fig_customer, use_container_width=True)

# row 4 --- col 3
with col12:
    st.subheader("🏆 Business Insights")

    # Best State
    best_state = (
        filtered_df.groupby("State/Province")["Sales"]
        .sum()
        .idxmax()
    )

    # Best Product
    best_product = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    # Best Factory
    best_factory = (
        filtered_df.groupby("Factory")["Sales"]
        .sum()
        .idxmax()
    )

    # Best Ship Mode
    best_ship = (
        filtered_df.groupby("Ship Mode")["Sales"]
        .sum()
        .idxmax()
    )

    # Fastest Average Shipping
    fastest_state = (
        filtered_df.groupby("State/Province")["Shipping Days"]
        .mean()
        .idxmin()
    )

    st.success(f"🏭 Best Factory\n\n**{best_factory}**")

    st.info(f"🌎 Highest Sales State\n\n**{best_state}**")

    st.warning(f"📦 Best Selling Product\n\n**{best_product}**")

    st.success(f"🚚 Best Ship Mode\n\n**{best_ship}**")

    st.info(f"⚡ Fastest Shipping State\n\n**{fastest_state}**")

st.divider()

# Download
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_shipping_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption(
    "Developed for Factory-to-Customer Shipping Route Efficiency Analysis"
)
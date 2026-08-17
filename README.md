# Factory-to-Customer Shipping Route Efficiency Analysis

An interactive data analytics and business intelligence project designed to analyze factory-to-customer shipping performance for the Nassau Candy Distributor dataset.

The project combines data cleaning, validation, exploratory data analysis, route analysis, geographic analysis, financial analysis, and interactive visualization into a Streamlit-based dashboard.

---

## 1. Project Overview

Efficient shipping operations are essential for maintaining customer satisfaction, controlling operational costs, and improving supply-chain performance.

This project analyzes historical shipping data to evaluate factory-to-customer routes, recorded shipping lead times, shipping modes, factory performance, regional performance, state-level trends, sales, and gross profit.

An interactive Streamlit dashboard has been developed to allow users to explore the data using dynamic filters and visualizations.

### Key Areas of Analysis

- Overall shipping performance
- Factory-to-state route efficiency
- Factory performance
- Shipping mode performance
- Regional and state-level performance
- Sales and gross profit
- Recorded shipping lead time
- Data quality and validation
- Potentially inefficient shipping patterns

---

## 2. Business Problem

Shipping performance can vary significantly across factories, routes, regions, states, and shipping modes.

Without a centralized analytical dashboard, it can be difficult to identify:

- Which routes perform efficiently
- Which routes show higher recorded lead times
- Which factories handle the highest shipment volumes
- Which shipping modes perform better
- Which regions generate higher sales and profit
- Whether the dataset contains quality issues affecting analysis

This project addresses these challenges by transforming raw shipping data into an interactive analytical dashboard.

---

## 3. Project Objectives

The primary objectives of this project are to:

1. Analyze overall shipping performance.
2. Evaluate factory-to-customer route efficiency.
3. Compare shipping performance across different shipping modes.
4. Measure factory-level operational performance.
5. Analyze regional and state-level shipping trends.
6. Evaluate sales and gross profit performance.
7. Identify unusual or potentially inefficient shipping patterns.
8. Perform data-quality and validation checks.
9. Present actionable insights through an interactive dashboard.

---

## 4. Data Quality Consideration

### Recorded Lead Time

A significant data-quality issue was identified during the analysis.

The dataset contains a multi-year gap between the `Order Date` and `Ship Date` for certain records.

Therefore, the calculated difference between these dates is treated as:

**Recorded Lead Time**

It should not be interpreted as the actual transportation or delivery duration.

The dashboard explicitly highlights this limitation and uses Recorded Lead Time primarily for comparative analysis and pattern identification.

This validation step is important because directly interpreting the date difference as actual delivery time could lead to misleading business conclusions.

---

## 5. Dataset

The project uses the **Nassau Candy Distributor Shipping Dataset**.

### Key Fields

| Category | Fields |
|---|---|
| Order Information | Order ID, Order Date |
| Shipping Information | Ship Date, Ship Mode, Shipping Lead Time |
| Customer Information | Customer ID, City, State/Province |
| Geographic Information | Country/Region, Region, Postal Code |
| Product Information | Product, Units, Cost |
| Financial Information | Sales, Gross Profit |
| Factory Information | Factory, Factory Latitude, Factory Longitude |

---

## 6. Technology Stack

| Technology | Usage |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning and transformation |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Matplotlib | Exploratory visualization |
| Seaborn | Statistical visualization |
| Streamlit | Interactive dashboard development |
| Jupyter Notebook | Exploratory Data Analysis |
| Git & GitHub | Version control and project management |

---

# 7. Analytical Methodology

The project follows a structured data analytics workflow.

### Step 1 — Data Preparation

The raw dataset is loaded and examined for:

- Missing values
- Duplicate records
- Incorrect data types
- Invalid dates
- Inconsistent values

### Step 2 — Data Cleaning

Data is cleaned and transformed using Pandas to prepare it for analysis.

### Step 3 — Data Validation

Validation checks are performed for:

- Missing Order Dates
- Missing Ship Dates
- Negative lead times
- Unusual date gaps
- Missing critical fields
- Inconsistent records

### Step 4 — Exploratory Data Analysis

The dataset is analyzed across:

- Factories
- Routes
- Shipping modes
- Regions
- States
- Sales
- Gross Profit
- Recorded Lead Time

### Step 5 — Route Analysis

Factory-to-state routes are evaluated using:

- Average Recorded Lead Time
- Median Recorded Lead Time
- Lead-time variability
- Shipment volume
- Sales
- Gross Profit

### Step 6 — Dashboard Development

The final analytical outputs are integrated into an interactive Streamlit dashboard.

---

# 8. Dashboard Features

## 8.1 Shipping Performance Overview

The dashboard provides key performance indicators such as:

- Total Orders
- Total Sales
- Gross Profit
- Average Recorded Lead Time
- Records Analyzed

These KPIs provide a high-level overview of the dataset and selected filters.

---

## 8.2 Interactive Filtering

Users can dynamically filter the analysis by:

- Order Date
- Region
- State
- Ship Mode

All relevant metrics and visualizations update according to the selected filters.

---

## 8.3 Data Quality & Validation

The dashboard includes a dedicated validation section covering:

- Missing dates
- Negative lead times
- Missing values
- Multi-year date gaps
- Potentially unusual records

This helps users understand the limitations of the dataset before interpreting the results.

---

## 8.4 Route Efficiency Analysis

The route analysis evaluates factory-to-state shipping performance.

The dashboard provides:

- Top 10 efficient routes
- Bottom 10 routes by recorded lead time
- Route performance rankings
- Average Recorded Lead Time
- Median Recorded Lead Time
- Lead-time variability
- Shipment volume
- Route-level financial performance

---

## 8.5 Factory Performance

Factory performance is evaluated using:

- Shipment volume
- Average Recorded Lead Time
- Sales
- Gross Profit

This allows users to compare operational and financial performance across factories.

---

## 8.6 Shipping Mode Analysis

The dashboard compares:

- First Class
- Same Day
- Second Class
- Standard Class

The analysis focuses on:

- Shipment volume
- Average Recorded Lead Time
- Relative shipping performance

---

## 8.7 Geographic Performance

Geographic analysis is performed at both regional and state levels.

Key metrics include:

- Orders
- Sales
- Gross Profit
- Average Recorded Lead Time

This enables users to identify geographic trends and areas requiring further investigation.

---

## 8.8 Financial Performance

The dashboard also evaluates the relationship between shipping activity and financial performance.

Analysis includes:

- Total Sales
- Gross Profit
- Factory-level financial performance
- Regional financial performance
- Route-level financial performance

---

# 9. Key Business Questions

The dashboard is designed to answer questions such as:

### Shipping

- What is the overall shipping performance?
- Which routes have the lowest Recorded Lead Time?
- Which routes have the highest Recorded Lead Time?
- Are there unusual lead-time patterns?

### Factory

- Which factory handles the highest shipment volume?
- Which factory generates the highest sales?
- Which factory generates the highest gross profit?
- How does factory performance vary?

### Shipping Mode

- How does Recorded Lead Time vary by shipping mode?
- Which shipping mode handles the highest shipment volume?
- Which shipping modes require further investigation?

### Geography

- Which region generates the highest sales?
- Which region generates the highest gross profit?
- Which states have the highest shipment volume?
- Which geographic areas show unusual shipping patterns?

### Data Quality

- Are there missing records?
- Are there invalid or negative lead times?
- Are there unusual Order Date–Ship Date gaps?
- How might data-quality issues affect interpretation?

---
### 10. Installation & Setup
Clone the Repository
git clone https://github.com/chandanib626/Factory-to-Customer-Shipping-Dashboard.git
Navigate to the Project Directory
cd Factory_to_customer_shipping_analysis
Create a Virtual Environment
macOS / Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt

If a requirements.txt file is not available:

pip install streamlit pandas numpy plotly matplotlib seaborn openpyxl
Run the Dashboard
streamlit run dashboard.py

The application will open in the browser through the local Streamlit server.

## 11. Project Deliverables

The repository contains:

Cleaned dataset
Exploratory Data Analysis notebook
Streamlit dashboard
Executive Summary
Project documentation
Data-quality validation
Interactive visualizations
## 12 . Business Value

This project demonstrates how raw operational data can be transformed into an interactive decision-support solution.

The dashboard enables users to:

Monitor shipping performance
Compare factories
Evaluate routes
Analyze shipping modes
Identify geographic trends
Examine financial performance
Detect data-quality issues
Prioritize areas for further investigation
## 13. Future Enhancements

Potential improvements include:

Machine Learning-based delivery delay prediction
Actual transportation-distance analysis
GPS-based route optimization
Transportation cost analysis
Real-time shipment tracking
Automated anomaly detection
Weather and traffic integration
Predictive supply-chain analytics
Automated business alerts
Advanced geographic mapping
## 14. Author

Chandani Bharti

Data Analytics | Python | SQL | Data Visualization | Streamlit

Project Repository

GitHub Repository:
https://github.com/chandanib626/Factory-to-Customer-Shipping-Dashboard

# 15. Dashboard Architecture

```text
                 Raw Dataset
                      |
                      v
              Data Cleaning
                      |
                      v
              Data Validation
                      |
                      v
          Exploratory Data Analysis
                      |
                      v
            Feature Engineering
                      |
                      v
          Route & Performance Analysis
                      |
                      v
            Interactive Visualizations
                      |
                      v
             Streamlit Dashboard
                      |
                      v
             Business Insights

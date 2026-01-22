# 🏦 Bank Customer Churn Analysis

A comprehensive Data Analyst portfolio project analyzing customer churn patterns in a banking dataset.

## 📊 Project Overview

This project demonstrates key Data Analyst skills including data cleaning, exploratory analysis, customer segmentation, KPI development, and actionable business insights.

### Key Components

| Component | Description | Status |
|-----------|-------------|--------|
| **Data Cleaning** | Missing values, duplicates, data types | ✅ Complete |
| **EDA** | Statistical analysis, distributions | ✅ Complete |
| **Churn Analysis** | Segment-based churn patterns | ✅ Complete |
| **Customer Segmentation** | Balance, Credit, Tenure segments | ✅ Complete |
| **Risk Scoring** | Customer risk level calculation | ✅ Complete |
| **KPI Dashboard** | Interactive Streamlit dashboard | ✅ Complete |
| **Recommendations** | Actionable business insights | ✅ Complete |

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Analysis

```bash
cd src
python churn_analysis.py
```

### Run Dashboard

```bash
cd dashboard
streamlit run app.py
```

## 📁 Project Structure

```
bank_churn_project/
├── data/
│   ├── raw/                      # Original dataset
│   │   └── Customer-Churn-Records.csv
│   ├── processed_churn_data.csv  # Cleaned data with segments
│   ├── kpi_summary.csv           # KPI metrics
│   └── churn_by_*.csv            # Segment analyses
├── src/
│   └── churn_analysis.py         # Main analysis script
├── dashboard/
│   └── app.py                    # Streamlit dashboard
├── reports/                      # Generated reports
├── requirements.txt
└── README.md
```

## 📈 Key Findings

### Overall Metrics
- **Total Customers:** 10,000
- **Churn Rate:** 20.38%
- **Balance at Risk:** $185.7M

### Highest Churn Segments

| Segment | Churn Rate | Finding |
|---------|------------|---------|
| **Customers with Complaints** | 99.5% | Most critical factor |
| **4 Products** | 100% | Product complexity issue |
| **3 Products** | 82.7% | Product complexity issue |
| **Age 51-60** | 56.2% | Needs targeted retention |
| **Germany** | 32.4% | Regional issue |
| **Inactive Members** | 26.9% | Engagement opportunity |

### Churned vs Retained Comparison

| Metric | Churned | Retained |
|--------|---------|----------|
| Avg Balance | $91,109 | $72,742 |
| Active Member % | 36% | 55% |
| Has Complaint % | 99.8% | 0.1% |

## 💡 Business Recommendations

1. **Complaint Management (Critical)**
   - 99.5% of complainants churn
   - Implement real-time tracking and fast resolution

2. **Germany Market Strategy**
   - Highest churn rate by geography
   - Conduct market research and competitor analysis

3. **Product Optimization**
   - 3-4 product customers have 82-100% churn
   - Simplify product portfolio

4. **Activation Campaigns**
   - Inactive members have 2x churn rate
   - Launch re-engagement programs

## 🛠️ Technologies Used

- **Python 3.10+**
- **pandas, numpy** - Data manipulation
- **matplotlib, seaborn** - Visualization
- **Streamlit** - Interactive dashboard
- **Plotly** - Interactive charts

## 📚 Skills Demonstrated

- ✅ Data Cleaning & Validation
- ✅ Exploratory Data Analysis (EDA)
- ✅ Customer Segmentation
- ✅ KPI Development & Tracking
- ✅ Statistical Analysis
- ✅ Data Visualization
- ✅ Business Insights & Recommendations
- ✅ Dashboard Development

## 👤 Author

**Burak**  
Junior Database Analyst | Data Analyst  
Izmir, Turkey

## 📄 License

MIT License

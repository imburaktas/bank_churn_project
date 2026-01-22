"""
Bank Customer Churn Dashboard
==============================
Interactive Streamlit Dashboard for Churn Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page config
st.set_page_config(
    page_title="Bank Customer Churn Analysis",
    page_icon="🏦",
    layout="wide"
)

# Get paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(PROJECT_DIR, 'data/processed_churn_data.csv'))
    kpi = pd.read_csv(os.path.join(PROJECT_DIR, 'data/kpi_summary.csv'))
    return df, kpi.iloc[0]

try:
    df, kpi = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Header
st.title("🏦 Bank Customer Churn Analysis")
st.markdown("---")

if not data_loaded:
    st.stop()

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select Page", 
    ["Executive Summary", "Churn Analysis", "Customer Segments", "Risk Analysis", "Recommendations"])

# Color scheme
COLORS = {
    'churned': '#e74c3c',
    'retained': '#2ecc71',
    'primary': '#3498db',
    'secondary': '#9b59b6',
    'warning': '#f39c12'
}

# =============================================================================
# PAGE 1: EXECUTIVE SUMMARY
# =============================================================================
if page == "Executive Summary":
    st.header("📈 Executive Summary")
    
    # KPI Cards Row 1
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Customers", f"{int(kpi['total_customers']):,}")
    with col2:
        st.metric("Churn Rate", f"{kpi['churn_rate']:.1f}%", delta="-2.3%", delta_color="inverse")
    with col3:
        st.metric("Retention Rate", f"{kpi['retention_rate']:.1f}%")
    with col4:
        st.metric("Avg Balance", f"${kpi['avg_balance']:,.0f}")
    with col5:
        st.metric("Balance at Risk", f"${kpi['balance_at_risk']/1e6:.1f}M")
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn Distribution")
        churn_counts = df['Churned'].value_counts()
        fig = px.pie(
            values=churn_counts.values,
            names=['Retained', 'Churned'],
            color_discrete_sequence=[COLORS['retained'], COLORS['churned']],
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Churn by Geography")
        geo_churn = df.groupby('Geography')['Churned'].agg(['count', 'sum', 'mean']).reset_index()
        geo_churn.columns = ['Geography', 'Total', 'Churned', 'ChurnRate']
        geo_churn['ChurnRate'] = geo_churn['ChurnRate'] * 100
        
        fig = px.bar(geo_churn, x='Geography', y='ChurnRate',
                     color='ChurnRate', color_continuous_scale='RdYlGn_r',
                     text=geo_churn['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn by Age Group")
        age_churn = df.groupby('AgeGroup')['Churned'].agg(['count', 'mean']).reset_index()
        age_churn.columns = ['AgeGroup', 'Count', 'ChurnRate']
        age_churn['ChurnRate'] = age_churn['ChurnRate'] * 100
        
        fig = px.bar(age_churn, x='AgeGroup', y='ChurnRate',
                     color='ChurnRate', color_continuous_scale='RdYlGn_r',
                     text=age_churn['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Churn by Activity Status")
        active_churn = df.groupby('IsActiveMember')['Churned'].agg(['count', 'mean']).reset_index()
        active_churn['Status'] = active_churn['IsActiveMember'].map({0: 'Inactive', 1: 'Active'})
        active_churn['ChurnRate'] = active_churn['mean'] * 100
        
        fig = px.bar(active_churn, x='Status', y='ChurnRate',
                     color='ChurnRate', color_continuous_scale='RdYlGn_r',
                     text=active_churn['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE 2: CHURN ANALYSIS
# =============================================================================
elif page == "Churn Analysis":
    st.header("🔍 Detailed Churn Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        geo_filter = st.multiselect("Geography", df['Geography'].unique(), default=df['Geography'].unique())
    with col2:
        gender_filter = st.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
    with col3:
        card_filter = st.multiselect("Card Type", df['CardType'].unique(), default=df['CardType'].unique())
    
    # Filter data
    filtered_df = df[
        (df['Geography'].isin(geo_filter)) & 
        (df['Gender'].isin(gender_filter)) &
        (df['CardType'].isin(card_filter))
    ]
    
    st.markdown(f"**Filtered Customers:** {len(filtered_df):,} | **Churn Rate:** {filtered_df['Churned'].mean()*100:.1f}%")
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn by Gender")
        gender_data = filtered_df.groupby('Gender')['Churned'].agg(['count', 'sum', 'mean']).reset_index()
        gender_data.columns = ['Gender', 'Total', 'Churned', 'ChurnRate']
        gender_data['ChurnRate'] = gender_data['ChurnRate'] * 100
        
        fig = px.bar(gender_data, x='Gender', y=['Total', 'Churned'],
                     barmode='group', color_discrete_sequence=[COLORS['primary'], COLORS['churned']])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Churn by Number of Products")
        prod_data = filtered_df.groupby('NumOfProducts')['Churned'].agg(['count', 'mean']).reset_index()
        prod_data.columns = ['NumOfProducts', 'Count', 'ChurnRate']
        prod_data['ChurnRate'] = prod_data['ChurnRate'] * 100
        
        fig = px.bar(prod_data, x='NumOfProducts', y='ChurnRate',
                     color='ChurnRate', color_continuous_scale='RdYlGn_r',
                     text=prod_data['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Complaint Impact
    st.subheader("🚨 Complaint Impact on Churn")
    col1, col2 = st.columns(2)
    
    with col1:
        complaint_data = filtered_df.groupby('HasComplaint')['Churned'].agg(['count', 'mean']).reset_index()
        complaint_data['Status'] = complaint_data['HasComplaint'].map({0: 'No Complaint', 1: 'Has Complaint'})
        complaint_data['ChurnRate'] = complaint_data['mean'] * 100
        
        fig = px.bar(complaint_data, x='Status', y='ChurnRate',
                     color='Status', color_discrete_map={'No Complaint': COLORS['retained'], 'Has Complaint': COLORS['churned']},
                     text=complaint_data['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Key Finding")
        st.error("""
        **99.5% of customers who complained churned!**
        
        This is the strongest predictor of churn in the dataset.
        
        **Recommendation:** 
        - Implement proactive complaint resolution
        - Set up early warning system for complaints
        - Prioritize customer satisfaction monitoring
        """)

# =============================================================================
# PAGE 3: CUSTOMER SEGMENTS
# =============================================================================
elif page == "Customer Segments":
    st.header("👥 Customer Segmentation")
    
    # Segment selector
    segment_type = st.selectbox("Select Segment Type", 
        ["Balance Segment", "Credit Score Segment", "Tenure Segment", "Age Group"])
    
    segment_map = {
        "Balance Segment": "BalanceSegment",
        "Credit Score Segment": "CreditSegment", 
        "Tenure Segment": "TenureSegment",
        "Age Group": "AgeGroup"
    }
    
    segment_col = segment_map[segment_type]
    
    # Segment analysis
    seg_data = df.groupby(segment_col).agg({
        'Churned': ['count', 'sum', 'mean'],
        'Balance': 'mean',
        'CreditScore': 'mean'
    }).round(2)
    seg_data.columns = ['Total', 'Churned', 'ChurnRate', 'AvgBalance', 'AvgCreditScore']
    seg_data['ChurnRate'] = (seg_data['ChurnRate'] * 100).round(1)
    seg_data = seg_data.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Churn Rate by {segment_type}")
        fig = px.bar(seg_data, x=segment_col, y='ChurnRate',
                     color='ChurnRate', color_continuous_scale='RdYlGn_r',
                     text=seg_data['ChurnRate'].astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"Customer Distribution by {segment_type}")
        fig = px.pie(seg_data, values='Total', names=segment_col,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment details table
    st.subheader("Segment Details")
    st.dataframe(seg_data, use_container_width=True, hide_index=True)

# =============================================================================
# PAGE 4: RISK ANALYSIS
# =============================================================================
elif page == "Risk Analysis":
    st.header("⚠️ Risk Analysis")
    
    # High risk customers
    st.subheader("High Risk Customer Profile")
    
    # Calculate risk score
    df['RiskScore'] = 0
    df.loc[df['HasComplaint'] == 1, 'RiskScore'] += 40
    df.loc[df['IsActiveMember'] == 0, 'RiskScore'] += 20
    df.loc[df['Geography'] == 'Germany', 'RiskScore'] += 15
    df.loc[df['NumOfProducts'].isin([1, 3, 4]), 'RiskScore'] += 15
    df.loc[df['Age'] > 50, 'RiskScore'] += 10
    
    df['RiskLevel'] = pd.cut(df['RiskScore'], bins=[-1, 20, 40, 60, 100],
                             labels=['Low', 'Medium', 'High', 'Critical'])
    
    # Risk distribution
    col1, col2 = st.columns(2)
    
    with col1:
        risk_dist = df['RiskLevel'].value_counts().reset_index()
        risk_dist.columns = ['RiskLevel', 'Count']
        
        fig = px.pie(risk_dist, values='Count', names='RiskLevel',
                     color='RiskLevel',
                     color_discrete_map={'Low': '#2ecc71', 'Medium': '#f39c12', 
                                        'High': '#e67e22', 'Critical': '#e74c3c'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Churn rate by risk level
        risk_churn = df.groupby('RiskLevel')['Churned'].agg(['count', 'mean']).reset_index()
        risk_churn.columns = ['RiskLevel', 'Count', 'ChurnRate']
        risk_churn['ChurnRate'] = risk_churn['ChurnRate'] * 100
        
        fig = px.bar(risk_churn, x='RiskLevel', y='ChurnRate',
                     color='RiskLevel',
                     color_discrete_map={'Low': '#2ecc71', 'Medium': '#f39c12', 
                                        'High': '#e67e22', 'Critical': '#e74c3c'},
                     text=risk_churn['ChurnRate'].round(1).astype(str) + '%')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Balance at risk
    st.markdown("---")
    st.subheader("💰 Balance at Risk by Segment")
    
    risk_balance = df.groupby('RiskLevel').agg({
        'Balance': 'sum',
        'Churned': 'sum'
    }).reset_index()
    risk_balance['ChurnedBalance'] = df[df['Churned']==1].groupby('RiskLevel')['Balance'].sum().values
    
    fig = px.bar(risk_balance, x='RiskLevel', y='Balance',
                 color='RiskLevel',
                 color_discrete_map={'Low': '#2ecc71', 'Medium': '#f39c12', 
                                    'High': '#e67e22', 'Critical': '#e74c3c'},
                 text=risk_balance['Balance'].apply(lambda x: f'${x/1e6:.1f}M'))
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis_title="Total Balance ($)")
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE 5: RECOMMENDATIONS
# =============================================================================
elif page == "Recommendations":
    st.header("💡 Business Recommendations")
    
    st.markdown("""
    Based on the analysis, here are the key recommendations to reduce customer churn:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        ### 🚨 1. COMPLAINT MANAGEMENT (Critical!)
        
        **Finding:** 99.5% of customers who complained churned
        
        **Actions:**
        - Implement real-time complaint tracking system
        - Set SLA for complaint resolution (24-48 hours)
        - Create dedicated retention team for complainants
        - Proactive follow-up after complaint resolution
        - Compensation program for valid complaints
        
        **Expected Impact:** High
        """)
        
        st.warning("""
        ### 🇩🇪 2. GERMANY MARKET STRATEGY
        
        **Finding:** Germany has 32.4% churn rate (vs 16% others)
        
        **Actions:**
        - Conduct market research in Germany
        - Analyze competitor offerings
        - Review pricing and fee structure
        - Localize customer service
        - Consider product customization
        
        **Expected Impact:** Medium-High
        """)
    
    with col2:
        st.info("""
        ### 📦 3. PRODUCT OPTIMIZATION
        
        **Finding:** 3-4 product customers have 82-100% churn
        
        **Actions:**
        - Review product bundling strategy
        - Simplify product portfolio
        - Improve cross-sell targeting
        - Create value-added bundles
        - Reduce complexity for customers
        
        **Expected Impact:** Medium
        """)
        
        st.success("""
        ### 👤 4. ACTIVATION CAMPAIGNS
        
        **Finding:** Inactive members have 26.9% churn (vs 14.3%)
        
        **Actions:**
        - Launch re-engagement campaigns
        - Gamification and rewards program
        - Personalized offers based on behavior
        - Regular touchpoints and communications
        - Mobile app engagement features
        
        **Expected Impact:** Medium
        """)
    
    st.markdown("---")
    
    # Priority matrix
    st.subheader("📊 Priority Matrix")
    
    priority_data = pd.DataFrame({
        'Initiative': ['Complaint Management', 'Germany Strategy', 'Product Optimization', 'Activation Campaigns', 'Age-based Programs'],
        'Impact': [95, 70, 60, 55, 45],
        'Effort': [40, 70, 50, 45, 35],
        'Priority': ['Critical', 'High', 'Medium', 'Medium', 'Low']
    })
    
    fig = px.scatter(priority_data, x='Effort', y='Impact', 
                     color='Priority', size=[40, 35, 30, 30, 25],
                     text='Initiative',
                     color_discrete_map={'Critical': '#e74c3c', 'High': '#f39c12', 
                                        'Medium': '#3498db', 'Low': '#2ecc71'})
    fig.update_traces(textposition='top center')
    fig.update_layout(xaxis_title="Implementation Effort", yaxis_title="Business Impact",
                     xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]))
    
    # Add quadrant lines
    fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Bank Customer Churn Analysis | Data Analyst Portfolio Project*")

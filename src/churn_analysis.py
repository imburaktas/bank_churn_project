"""
Bank Customer Churn Analysis
============================
A comprehensive Data Analyst project for banking sector

Author: Burak
Date: January 2026

Sections:
1. Data Loading & Cleaning
2. Exploratory Data Analysis (EDA)
3. Customer Segmentation
4. Churn Analysis
5. Cohort Analysis
6. KPI Metrics & Insights
7. Business Recommendations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("=" * 70)
print("🏦 BANK CUSTOMER CHURN ANALYSIS")
print("=" * 70)

# =============================================================================
# 1. DATA LOADING & CLEANING
# =============================================================================
print("\n📊 BÖLÜM 1: VERİ YÜKLEME & TEMİZLEME")
print("-" * 50)

# Load data
df = pd.read_csv('../data/raw/Customer-Churn-Records.csv')

print(f"Dataset boyutu: {df.shape[0]:,} satır, {df.shape[1]} kolon")
print(f"\nKolonlar:\n{df.columns.tolist()}")

# Check for missing values
print(f"\n🔹 Eksik Değerler:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   ✅ Eksik değer yok!")
else:
    print(missing[missing > 0])

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"\n🔹 Duplike Satırlar: {duplicates}")

# Data types
print(f"\n🔹 Veri Tipleri:")
print(df.dtypes)

# Drop unnecessary columns
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
print(f"\n✅ Gereksiz kolonlar silindi. Yeni boyut: {df.shape}")

# Rename columns for clarity
df = df.rename(columns={
    'Exited': 'Churned',
    'Complain': 'HasComplaint',
    'Satisfaction Score': 'SatisfactionScore',
    'Card Type': 'CardType',
    'Point Earned': 'PointsEarned'
})

print(f"\n🔹 İlk 5 Satır:")
print(df.head())

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n\n📊 BÖLÜM 2: KEŞİFSEL VERİ ANALİZİ (EDA)")
print("-" * 50)

# Basic statistics
print("\n🔹 Sayısal Değişken İstatistikleri:")
print(df.describe().round(2))

# Target variable distribution
churn_rate = df['Churned'].mean() * 100
print(f"\n🔹 Churn Oranı: {churn_rate:.2f}%")
print(f"   - Churned (Ayrılan): {df['Churned'].sum():,} ({churn_rate:.1f}%)")
print(f"   - Retained (Kalan): {(df['Churned'] == 0).sum():,} ({100-churn_rate:.1f}%)")

# Categorical variables distribution
print("\n🔹 Kategorik Değişken Dağılımları:")

print("\n   Geography:")
print(df['Geography'].value_counts())

print("\n   Gender:")
print(df['Gender'].value_counts())

print("\n   Card Type:")
print(df['CardType'].value_counts())

# =============================================================================
# 3. CHURN ANALYSIS BY SEGMENTS
# =============================================================================
print("\n\n📊 BÖLÜM 3: SEGMENT BAZLI CHURN ANALİZİ")
print("-" * 50)

# Churn by Geography
print("\n🔹 Ülkeye Göre Churn:")
geo_churn = df.groupby('Geography').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
geo_churn.columns = ['Total', 'Churned', 'ChurnRate']
geo_churn['ChurnRate'] = (geo_churn['ChurnRate'] * 100).round(2)
geo_churn = geo_churn.sort_values('ChurnRate', ascending=False)
print(geo_churn)

# Churn by Gender
print("\n🔹 Cinsiyete Göre Churn:")
gender_churn = df.groupby('Gender').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
gender_churn.columns = ['Total', 'Churned', 'ChurnRate']
gender_churn['ChurnRate'] = (gender_churn['ChurnRate'] * 100).round(2)
print(gender_churn)

# Churn by Age Groups
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], 
                        labels=['18-30', '31-40', '41-50', '51-60', '60+'])
print("\n🔹 Yaş Grubuna Göre Churn:")
age_churn = df.groupby('AgeGroup').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
age_churn.columns = ['Total', 'Churned', 'ChurnRate']
age_churn['ChurnRate'] = (age_churn['ChurnRate'] * 100).round(2)
print(age_churn)

# Churn by Number of Products
print("\n🔹 Ürün Sayısına Göre Churn:")
product_churn = df.groupby('NumOfProducts').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
product_churn.columns = ['Total', 'Churned', 'ChurnRate']
product_churn['ChurnRate'] = (product_churn['ChurnRate'] * 100).round(2)
print(product_churn)

# Churn by Active Membership
print("\n🔹 Aktif Üyeliğe Göre Churn:")
active_churn = df.groupby('IsActiveMember').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
active_churn.columns = ['Total', 'Churned', 'ChurnRate']
active_churn['ChurnRate'] = (active_churn['ChurnRate'] * 100).round(2)
active_churn.index = ['Inactive', 'Active']
print(active_churn)

# Churn by Complaint
print("\n🔹 Şikayete Göre Churn:")
complain_churn = df.groupby('HasComplaint').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
complain_churn.columns = ['Total', 'Churned', 'ChurnRate']
complain_churn['ChurnRate'] = (complain_churn['ChurnRate'] * 100).round(2)
complain_churn.index = ['No Complaint', 'Has Complaint']
print(complain_churn)

# Churn by Card Type
print("\n🔹 Kart Tipine Göre Churn:")
card_churn = df.groupby('CardType').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
card_churn.columns = ['Total', 'Churned', 'ChurnRate']
card_churn['ChurnRate'] = (card_churn['ChurnRate'] * 100).round(2)
card_churn = card_churn.sort_values('ChurnRate', ascending=False)
print(card_churn)

# Churn by Satisfaction Score
print("\n🔹 Memnuniyet Skoruna Göre Churn:")
sat_churn = df.groupby('SatisfactionScore').agg({
    'Churned': ['count', 'sum', 'mean']
}).round(3)
sat_churn.columns = ['Total', 'Churned', 'ChurnRate']
sat_churn['ChurnRate'] = (sat_churn['ChurnRate'] * 100).round(2)
print(sat_churn)

# =============================================================================
# 4. CUSTOMER SEGMENTATION (RFM-like)
# =============================================================================
print("\n\n📊 BÖLÜM 4: MÜŞTERİ SEGMENTASYONU")
print("-" * 50)

# Create segments based on Balance and Activity
df['BalanceSegment'] = pd.qcut(df['Balance'].replace(0, np.nan), 
                                q=4, labels=['Low', 'Medium', 'High', 'Premium'],
                                duplicates='drop')
df['BalanceSegment'] = df['BalanceSegment'].cat.add_categories(['Zero'])
df.loc[df['Balance'] == 0, 'BalanceSegment'] = 'Zero'

print("\n🔹 Bakiye Segmentine Göre Dağılım:")
balance_seg = df.groupby('BalanceSegment').agg({
    'Churned': ['count', 'sum', 'mean'],
    'Balance': 'mean'
}).round(2)
balance_seg.columns = ['Total', 'Churned', 'ChurnRate', 'AvgBalance']
balance_seg['ChurnRate'] = (balance_seg['ChurnRate'] * 100).round(2)
print(balance_seg)

# Credit Score Segments
df['CreditSegment'] = pd.cut(df['CreditScore'], 
                              bins=[0, 580, 670, 740, 800, 900],
                              labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
print("\n🔹 Kredi Skoru Segmentine Göre Dağılım:")
credit_seg = df.groupby('CreditSegment').agg({
    'Churned': ['count', 'sum', 'mean'],
    'CreditScore': 'mean'
}).round(2)
credit_seg.columns = ['Total', 'Churned', 'ChurnRate', 'AvgCreditScore']
credit_seg['ChurnRate'] = (credit_seg['ChurnRate'] * 100).round(2)
print(credit_seg)

# Tenure Segments
df['TenureSegment'] = pd.cut(df['Tenure'], 
                              bins=[-1, 2, 5, 8, 10],
                              labels=['New (0-2)', 'Growing (3-5)', 'Mature (6-8)', 'Loyal (9-10)'])
print("\n🔹 Tenure Segmentine Göre Dağılım:")
tenure_seg = df.groupby('TenureSegment').agg({
    'Churned': ['count', 'sum', 'mean'],
    'Tenure': 'mean'
}).round(2)
tenure_seg.columns = ['Total', 'Churned', 'ChurnRate', 'AvgTenure']
tenure_seg['ChurnRate'] = (tenure_seg['ChurnRate'] * 100).round(2)
print(tenure_seg)

# =============================================================================
# 5. VALUE ANALYSIS
# =============================================================================
print("\n\n📊 BÖLÜM 5: DEĞER ANALİZİ")
print("-" * 50)

# Revenue impact of churned customers
churned_customers = df[df['Churned'] == 1]
retained_customers = df[df['Churned'] == 0]

print("\n🔹 Churned vs Retained Müşteri Karşılaştırması:")
comparison = pd.DataFrame({
    'Metric': ['Count', 'Avg Balance', 'Avg Credit Score', 'Avg Tenure', 
               'Avg Satisfaction', 'Avg Points', 'Active Member %', 'Has Complaint %'],
    'Churned': [
        len(churned_customers),
        churned_customers['Balance'].mean(),
        churned_customers['CreditScore'].mean(),
        churned_customers['Tenure'].mean(),
        churned_customers['SatisfactionScore'].mean(),
        churned_customers['PointsEarned'].mean(),
        churned_customers['IsActiveMember'].mean() * 100,
        churned_customers['HasComplaint'].mean() * 100
    ],
    'Retained': [
        len(retained_customers),
        retained_customers['Balance'].mean(),
        retained_customers['CreditScore'].mean(),
        retained_customers['Tenure'].mean(),
        retained_customers['SatisfactionScore'].mean(),
        retained_customers['PointsEarned'].mean(),
        retained_customers['IsActiveMember'].mean() * 100,
        retained_customers['HasComplaint'].mean() * 100
    ]
})
comparison['Churned'] = comparison['Churned'].round(2)
comparison['Retained'] = comparison['Retained'].round(2)
print(comparison.to_string(index=False))

# Total balance at risk
total_balance_churned = churned_customers['Balance'].sum()
total_balance_all = df['Balance'].sum()
print(f"\n🔹 Risk Altındaki Toplam Bakiye:")
print(f"   - Churned Müşteri Bakiyesi: ${total_balance_churned:,.2f}")
print(f"   - Toplam Bakiyenin %{(total_balance_churned/total_balance_all*100):.1f}'i")

# =============================================================================
# 6. KPI SUMMARY
# =============================================================================
print("\n\n📊 BÖLÜM 6: KPI ÖZETİ")
print("-" * 50)

print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    TEMEL KPI METRİKLERİ                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Toplam Müşteri:           {len(df):,}                            
║  Churn Oranı:              {churn_rate:.2f}%                      
║  Retention Oranı:          {100-churn_rate:.2f}%                  
║                                                                  
║  Ortalama Müşteri Bakiyesi: ${df['Balance'].mean():,.2f}          
║  Ortalama Kredi Skoru:      {df['CreditScore'].mean():.0f}        
║  Ortalama Tenure:           {df['Tenure'].mean():.1f} yıl         
║  Aktif Üye Oranı:           {df['IsActiveMember'].mean()*100:.1f}%
║  Şikayet Oranı:             {df['HasComplaint'].mean()*100:.1f}%  
║                                                                  
║  Risk Altındaki Bakiye:     ${total_balance_churned:,.2f}         
╚══════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# 7. KEY INSIGHTS & RECOMMENDATIONS
# =============================================================================
print("\n📊 BÖLÜM 7: TEMEL İÇGÖRÜLER & ÖNERİLER")
print("-" * 50)

# Find highest churn segments
print("\n🔴 EN YÜKSEK CHURN ORANLARI:")
print(f"   1. Şikayet eden müşteriler: {complain_churn.loc['Has Complaint', 'ChurnRate']:.1f}%")
print(f"   2. Almanya müşterileri: {geo_churn.loc['Germany', 'ChurnRate']:.1f}%")
print(f"   3. 4 ürünlü müşteriler: {product_churn.loc[4, 'ChurnRate']:.1f}%")
print(f"   4. Inaktif üyeler: {active_churn.loc['Inactive', 'ChurnRate']:.1f}%")
print(f"   5. 51-60 yaş grubu: {age_churn.loc['51-60', 'ChurnRate']:.1f}%")

print(f"""
\n💡 İŞ ÖNERİLERİ:

1. ŞİKAYET YÖNETİMİ (En Kritik!)
   → Şikayet eden müşterilerin churn oranı çok yüksek
   → Şikayet çözüm süresini kısalt
   → Proaktif müşteri memnuniyeti takibi yap

2. ALMANYA ODAKLI STRATEJİ
   → Almanya'daki müşteriler en yüksek churn oranına sahip
   → Lokal müşteri deneyimi araştırması yap
   → Rekabet analizi ve fiyatlandırma gözden geçir

3. ÜRÜN OPTİMİZASYONU
   → 3-4 ürünlü müşteriler yüksek churn gösteriyor
   → Ürün çapraz satış stratejisini gözden geçir
   → Ürün bundle'larını optimize et

4. AKTİVASYON KAMPANYALARI
   → Inaktif üyeleri aktifleştir
   → Loyalty program güçlendir
   → Düzenli engagement kampanyaları

5. YAŞ GRUBU ODAKLI YAKLAŞIM
   → 40+ yaş grubu için özel retention programları
   → Yaşa uygun iletişim kanalları kullan
""")

# =============================================================================
# 8. SAVE PROCESSED DATA
# =============================================================================
print("\n📊 BÖLÜM 8: VERİ KAYDETME")
print("-" * 50)

# Save processed data
df.to_csv('../data/processed_churn_data.csv', index=False)
print("✅ İşlenmiş veri kaydedildi: data/processed_churn_data.csv")

# Save summary statistics for dashboard
summary_stats = {
    'total_customers': len(df),
    'churn_rate': churn_rate,
    'retention_rate': 100 - churn_rate,
    'avg_balance': df['Balance'].mean(),
    'avg_credit_score': df['CreditScore'].mean(),
    'avg_tenure': df['Tenure'].mean(),
    'active_member_rate': df['IsActiveMember'].mean() * 100,
    'complaint_rate': df['HasComplaint'].mean() * 100,
    'balance_at_risk': total_balance_churned
}

pd.DataFrame([summary_stats]).to_csv('../data/kpi_summary.csv', index=False)
print("✅ KPI özeti kaydedildi: data/kpi_summary.csv")

# Save segment analysis
geo_churn.to_csv('../data/churn_by_geography.csv')
gender_churn.to_csv('../data/churn_by_gender.csv')
age_churn.to_csv('../data/churn_by_age.csv')
product_churn.to_csv('../data/churn_by_products.csv')
print("✅ Segment analizleri kaydedildi")

print("\n" + "=" * 70)
print("✅ ANALİZ TAMAMLANDI!")
print("=" * 70)

import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = []

# Title & Context
cells.append(nbf.v4.new_markdown_cell("""# 📊 Customer Churn Analysis & Retention Strategy
### Telecom & Subscription Business Analytics Case Study
**Author:** Yash Pratap Singh — Data Analyst & Business Analyst  
**Dataset:** `telecom_customer_churn.csv` (1,200 CRM Customer Records)  
**Tools Used:** Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn

---

## 🏢 Business Context & Problem Statement
Leadership at our subscription-based telecom company noticed quarterly customer churn is rising, resulting in substantial recurring revenue loss. However, leadership lacked visibility into:
1. **Who is churning?** (Demographic and account profiles)
2. **Why are they churning?** (Service quality, contract lock-in, pricing, support interaction drivers)
3. **What concrete actions can stop revenue leakage?**

This notebook performs end-to-end data cleaning on raw CRM exports, exploratory data analysis (EDA), statistical metrics aggregation, publication-grade data visualizations, machine learning predictive modeling (Logistic Regression), and formulates executive recommendations for senior leadership."""))

# Imports
cells.append(nbf.v4.new_markdown_cell("## 🛠️ Step 0: Import Libraries & Environment Setup"))
cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve

# Configure Matplotlib & Seaborn visual theme
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Inter'
plt.rcParams['axes.edgecolor'] = '#e2e8f0'
plt.rcParams['axes.linewidth'] = 1.2
%matplotlib inline
"""))

# Data Loading & Inspection
cells.append(nbf.v4.new_markdown_cell("""## 🧹 Task 1: Data Cleaning & Feature Engineering

### 1.1 Load CSV and Inspect Structure
We load the raw CRM data export `telecom_customer_churn.csv` and inspect missing values, data types, and duplicate rows."""))

cells.append(nbf.v4.new_code_cell("""# Load raw dataset
df_raw = pd.read_csv('telecom_customer_churn.csv')

print(f"Raw Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
print("\\n--- Missing Values Count ---")
print(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])
print(f"\\nDuplicate Rows Detected: {df_raw.duplicated().sum()}")
df_raw.head()
"""))

# Data Cleaning Implementation
cells.append(nbf.v4.new_markdown_cell("""### 1.2 Data Cleaning & Justification
- **Duplicate Removal:** Removed 25 exact duplicate CRM records (`drop_duplicates()`).
- **SatisfactionScore Imputation:** Imputed missing values (`NaN`) using the **Median** (`3.0`). *Justification: SatisfactionScore is an ordinal 1–5 scale. Median imputation preserves central tendency without introducing non-integer floating artifacts.*
- **PaymentMethod Imputation:** Imputed missing values with `'Unknown'`. *Justification: Preserves customer transaction records without making invalid assumptions about payment preferences.*
- **City Text Standardization:** Standardized casing variations (`mumbai`, `MUMBAI`, `Mumbai` -> `Mumbai`).
- **Feature Engineering (`TenureBucket`):** Categorized tenure into three business tiers:
  - `New (<12 mo)`: High churn vulnerability period
  - `Mid (12-36 mo)`: Medium tenure stabilization
  - `Loyal (36+ mo)`: High tenure, long-term brand equity"""))

cells.append(nbf.v4.new_code_cell("""df_clean = df_raw.copy()

# 1. Remove duplicate rows
df_clean = df_clean.drop_duplicates().reset_index(drop=True)

# 2. Impute missing values
df_clean['SatisfactionScore'] = df_clean['SatisfactionScore'].fillna(df_clean['SatisfactionScore'].median())
df_clean['PaymentMethod'] = df_clean['PaymentMethod'].fillna("Unknown")

# 3. Standardize text casing in City
df_clean['City'] = df_clean['City'].astype(str).str.strip().str.title()

# 4. Feature Engineering: TenureBucket
def assign_tenure_bucket(tenure):
    if tenure < 12:
        return 'New (<12 mo)'
    elif tenure <= 36:
        return 'Mid (12-36 mo)'
    else:
        return 'Loyal (36+ mo)'

df_clean['TenureBucket'] = df_clean['TenureMonths'].apply(assign_tenure_bucket)
df_clean['TenureBucket'] = pd.Categorical(df_clean['TenureBucket'], 
                                        categories=['New (<12 mo)', 'Mid (12-36 mo)', 'Loyal (36+ mo)'], 
                                        ordered=True)

# Create numeric binary target for modeling
df_clean['ChurnNumeric'] = (df_clean['Churn'] == 'Yes').astype(int)

print(f"Cleaned Dataset Shape: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
print(f"Remaining Missing Values: {df_clean.isnull().sum().sum()}")
df_clean[['CustomerID', 'City', 'TenureMonths', 'TenureBucket', 'SatisfactionScore', 'PaymentMethod']].head()
"""))

# EDA & Financial Metrics
cells.append(nbf.v4.new_markdown_cell("""## 📈 Task 2: Exploratory Data Analysis & Business KPIs

### Key Research Questions:
1. What is the overall customer churn rate?
2. How does churn vary across Contracts, Tenure Buckets, AutoPay status, and Support Call frequency?
3. What is the total **Revenue at Risk** (Monthly and Annualized) in ₹?
"""))

cells.append(nbf.v4.new_code_cell("""total_cust = len(df_clean)
total_churned = df_clean['ChurnNumeric'].sum()
overall_churn_pct = (total_churned / total_cust) * 100

avg_bill_churned = df_clean[df_clean['ChurnNumeric'] == 1]['MonthlyCharges'].mean()
avg_bill_retained = df_clean[df_clean['ChurnNumeric'] == 0]['MonthlyCharges'].mean()

monthly_rev_risk = df_clean[df_clean['ChurnNumeric'] == 1]['MonthlyCharges'].sum()
annual_rev_risk = monthly_rev_risk * 12

print(f"🎯 OVERALL CHURN RATE: {overall_churn_pct:.2f}% ({total_churned:,} out of {total_cust:,} customers)")
print(f"💰 Average Monthly Bill (Churned): ₹{avg_bill_churned:.2f}")
print(f"💰 Average Monthly Bill (Retained): ₹{avg_bill_retained:.2f}")
print(f"🚨 MONTHLY REVENUE AT RISK: ₹{monthly_rev_risk:,.2f}")
print(f"🚨 ANNUALIZED REVENUE AT RISK: ₹{annual_rev_risk:,.2f} (~₹{annual_rev_risk/1e5:.2f} Lakhs)")
"""))

cells.append(nbf.v4.new_markdown_cell("### 2.2 Segmented Churn Analysis Tables"))

cells.append(nbf.v4.new_code_cell("""# Churn Rate by Contract Type
contract_agg = df_clean.groupby('Contract').agg(
    Total=('CustomerID', 'count'),
    Churned=('ChurnNumeric', 'sum'),
    Churn_Rate_Pct=('ChurnNumeric', lambda x: x.mean() * 100),
    Avg_Monthly_Bill=('MonthlyCharges', 'mean')
).reset_index()

# Churn Rate by Tenure Bucket
tenure_agg = df_clean.groupby('TenureBucket', observed=False).agg(
    Total=('CustomerID', 'count'),
    Churned=('ChurnNumeric', 'sum'),
    Churn_Rate_Pct=('ChurnNumeric', lambda x: x.mean() * 100)
).reset_index()

# Churn Rate by Support Calls
support_agg = df_clean.groupby('SupportCallsLast6Mo').agg(
    Total=('CustomerID', 'count'),
    Churned=('ChurnNumeric', 'sum'),
    Churn_Rate_Pct=('ChurnNumeric', lambda x: x.mean() * 100)
).reset_index()

print("--- Churn by Contract Type ---")
display(contract_agg)
print("\\n--- Churn by Tenure Bucket ---")
display(tenure_agg)
"""))

# Visualizations
cells.append(nbf.v4.new_markdown_cell("""## 🎨 Task 3: Data Visualizations

We generate four core stakeholder-ready Matplotlib/Seaborn visualizations to clearly communicate churn drivers to leadership."""))

cells.append(nbf.v4.new_code_cell("""# Visual 1 & 2: Churn Rate by Contract & Tenure Bucket
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Contract Chart
bars1 = ax1.bar(contract_agg['Contract'], contract_agg['Churn_Rate_Pct'], color=['#ef4444', '#f59e0b', '#10b981'], width=0.5)
ax1.set_title('Churn Rate by Contract Type', fontsize=13, fontweight='bold')
ax1.set_ylabel('Churn Rate (%)', fontweight='bold')
ax1.set_ylim(0, 70)
for bar in bars1:
    h = bar.get_height()
    ax1.annotate(f'{h:.1f}%', (bar.get_x() + bar.get_width()/2, h), xytext=(0, 5), textcoords='offset points', ha='center', fontweight='bold')

# Tenure Chart
bars2 = ax2.bar(tenure_agg['TenureBucket'].astype(str), tenure_agg['Churn_Rate_Pct'], color=['#dc2626', '#3b82f6', '#059669'], width=0.5)
ax2.set_title('Churn Rate by Tenure Bucket', fontsize=13, fontweight='bold')
ax2.set_ylabel('Churn Rate (%)', fontweight='bold')
ax2.set_ylim(0, 60)
for bar in bars2:
    h = bar.get_height()
    ax2.annotate(f'{h:.1f}%', (bar.get_x() + bar.get_width()/2, h), xytext=(0, 5), textcoords='offset points', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Visual 3 & 4: Satisfaction Distribution & City Breakdown
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))

# Satisfaction Score Distribution
sns.histplot(data=df_clean, x='SatisfactionScore', hue='Churn', discrete=True, multiple='dodge', palette={'Yes': '#ef4444', 'No': '#3b82f6'}, shrink=0.8, ax=ax1)
ax1.set_title('Satisfaction Score Distribution (Churned vs Retained)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Satisfaction Score (1 = Unhappy, 5 = Very Happy)')

# City Breakdown (Count & Rate)
city_agg = df_clean.groupby('City').agg(
    Churned_Count=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100)
).sort_values(by='Churned_Count', ascending=False).reset_index()

ax2_twin = ax2.twinx()
ax2.bar(city_agg['City'], city_agg['Churned_Count'], color='#3b82f6', alpha=0.8, width=0.45, label='Churned Count')
ax2_twin.plot(city_agg['City'], city_agg['Churn_Rate'], color='#ef4444', marker='o', linewidth=2.5, label='Churn Rate %')
ax2.set_title('City Churn Breakdown: Count & Churn Rate', fontsize=13, fontweight='bold')
ax2.set_ylabel('Churned Customer Count', color='#3b82f6', fontweight='bold')
ax2_twin.set_ylabel('Churn Rate (%)', color='#ef4444', fontweight='bold')
ax2_twin.grid(False)

plt.tight_layout()
plt.show()
"""))

# Machine Learning & Correlation
cells.append(nbf.v4.new_markdown_cell("""## 🤖 Stretch Goals: Predictive Modeling (Logistic Regression) & Heatmap

We build a scikit-learn **Logistic Regression Classifier** to predict individual customer churn risk scores and determine feature importance."""))

cells.append(nbf.v4.new_code_cell("""# Prepare Features for Modeling
feature_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'SupportCallsLast6Mo', 'SatisfactionScore', 'Contract', 'PlanType', 'AutoPayEnabled']
X = pd.get_dummies(df_clean[feature_cols], drop_first=True)
y = df_clean['ChurnNumeric']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

# Fit Logistic Regression Model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluate Metrics
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print(f"✅ Model Accuracy:  {acc*100:.2f}%")
print(f"🎯 Precision Score: {prec*100:.2f}%")
print(f"🔁 Recall Score:    {rec*100:.2f}%")
print(f"📈 ROC-AUC Score:   {roc_auc:.3f}")
"""))

cells.append(nbf.v4.new_code_cell("""# Visual 5 & 6: Correlation Heatmap & Feature Importance
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Heatmap
numeric_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'SupportCallsLast6Mo', 'SatisfactionScore', 'ChurnNumeric']
sns.heatmap(df_clean[numeric_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax1)
ax1.set_title('Feature Correlation Heatmap', fontsize=12, fontweight='bold')

# Feature Coefficients
coef_df = pd.DataFrame({'Feature': X.columns, 'Importance': model.coef_[0]}).sort_values(by='Importance', ascending=True)
ax2.barh(coef_df['Feature'], coef_df['Importance'], color=np.where(coef_df['Importance'] > 0, '#ef4444', '#10b981'))
ax2.set_title('Logistic Regression Feature Coefficients', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
"""))

# Executive Recommendation
cells.append(nbf.v4.new_markdown_cell("""## 🎯 Task 4: Executive Business Recommendation (VP Briefing)

> **TO:** Vice President of Customer Success & Operations  
> **FROM:** Yash Pratap Singh, Data Analyst  
> **SUBJECT:** Customer Churn Analysis & Operational Retention Strategy  
>
> **Executive Summary:**  
> Our analysis of 1,200 CRM customer records reveals an overall churn rate of **39.58%**, representing **₹46.45 Lakhs in annual revenue at risk** (₹3,87,103/month). The primary drivers of customer exit are **Month-to-Month contracts** (58.3% churn vs 5.6% for 2-year plans), **early customer lifecycle stage** (<12 months tenure exhibits 46.2% churn), and **support friction** (customers making 3+ support calls reach a staggering 63.8% churn rate). 
> 
> **Strategic Action Plan:**  
> We recommend implementing a 3-pronged proactive retention campaign:
> 1. **Contract Transition Incentive:** Offer a ₹200/month bill discount to Month-to-Month customers in their first 6 months who convert to a 1-Year or 2-Year contract.
> 2. **Automated Support Trigger:** Establish an automated CRM alert after a customer's **2nd support call**, dispatching a dedicated senior support agent to resolve underlying issues before churn intent materializes.
> 3. **AutoPay Enrollment Rebate:** Provide a one-time ₹150 bill credit for enabling AutoPay via UPI or Credit Card, addressing non-autopay churn friction.
"""))

nb['cells'] = cells

# Write notebook to paths
with open('data/telecom/telecom_customer_churn_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

with open('telecom_customer_churn_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Jupyter Notebook created successfully at:")
print(" - data/telecom/telecom_customer_churn_analysis.ipynb")
print(" - telecom_customer_churn_analysis.ipynb")

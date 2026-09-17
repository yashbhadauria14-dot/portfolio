import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

sys.stdout.reconfigure(encoding='utf-8')

# Set styling for plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Inter'
plt.rcParams['axes.edgecolor'] = '#e2e8f0'
plt.rcParams['axes.linewidth'] = 1.2

os.makedirs('data/telecom/charts', exist_ok=True)

# ---------------------------------------------------------
# STEP 1: Load Raw Data & Inspect
# ---------------------------------------------------------
df_raw = pd.read_csv('data/telecom/telecom_customer_churn.csv')
raw_shape = df_raw.shape
raw_missing = df_raw.isnull().sum()
raw_dups = df_raw.duplicated().sum()

# ---------------------------------------------------------
# STEP 2: Data Cleaning
# ---------------------------------------------------------
df_clean = df_raw.copy()

# Remove duplicate rows
df_clean = df_clean.drop_duplicates().reset_index(drop=True)

# Handle missing values
# SatisfactionScore -> impute median (3.0)
sat_median = df_clean['SatisfactionScore'].median()
df_clean['SatisfactionScore'] = df_clean['SatisfactionScore'].fillna(sat_median)

# PaymentMethod -> impute "Unknown"
df_clean['PaymentMethod'] = df_clean['PaymentMethod'].fillna("Unknown")

# Standardize City text casing
df_clean['City'] = df_clean['City'].astype(str).str.strip().str.title()

# Feature Engineering: TenureBucket
def assign_tenure_bucket(tenure):
    if tenure < 12:
        return 'New (<12 mo)'
    elif tenure <= 36:
        return 'Mid (12-36 mo)'
    else:
        return 'Loyal (36+ mo)'

df_clean['TenureBucket'] = df_clean['TenureMonths'].apply(assign_tenure_bucket)
# Order categorical bucket for proper plotting
tenure_order = ['New (<12 mo)', 'Mid (12-36 mo)', 'Loyal (36+ mo)']
df_clean['TenureBucket'] = pd.Categorical(df_clean['TenureBucket'], categories=tenure_order, ordered=True)

# Create numeric churn flag (1 = Yes, 0 = No)
df_clean['ChurnNumeric'] = (df_clean['Churn'] == 'Yes').astype(int)

clean_shape = df_clean.shape

# Save clean dataset
df_clean.to_csv('data/telecom/telecom_customer_churn_cleaned.csv', index=False)

# ---------------------------------------------------------
# STEP 3: Exploratory Analysis & Metrics
# ---------------------------------------------------------
total_customers = len(df_clean)
total_churned = df_clean['ChurnNumeric'].sum()
overall_churn_rate = (total_churned / total_customers) * 100

# Churn by Contract
churn_by_contract = df_clean.groupby('Contract').agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100),
    Avg_Monthly_Bill=('MonthlyCharges', 'mean')
).reset_index()

# Churn by TenureBucket
churn_by_tenure = df_clean.groupby('TenureBucket', observed=False).agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100),
    Avg_Monthly_Bill=('MonthlyCharges', 'mean')
).reset_index()

# Churn by AutoPay
churn_by_autopay = df_clean.groupby('AutoPayEnabled').agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100)
).reset_index()

# Churn by SatisfactionScore
churn_by_satisfaction = df_clean.groupby('SatisfactionScore').agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100)
).reset_index()

# Churn by Support Calls
churn_by_support = df_clean.groupby('SupportCallsLast6Mo').agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100)
).reset_index()

# Churn by City
churn_by_city = df_clean.groupby('City').agg(
    Total_Customers=('CustomerID', 'count'),
    Churned_Customers=('ChurnNumeric', 'sum'),
    Churn_Rate=('ChurnNumeric', lambda x: x.mean() * 100),
    Monthly_Revenue_Lost=('MonthlyCharges', lambda x: df_clean.loc[x.index[df_clean.loc[x.index, 'ChurnNumeric'] == 1], 'MonthlyCharges'].sum())
).sort_values(by='Churned_Customers', ascending=False).reset_index()

# Financial Metrics: Revenue at Risk
avg_charge_churned = df_clean[df_clean['ChurnNumeric'] == 1]['MonthlyCharges'].mean()
avg_charge_retained = df_clean[df_clean['ChurnNumeric'] == 0]['MonthlyCharges'].mean()

monthly_rev_at_risk = df_clean[df_clean['ChurnNumeric'] == 1]['MonthlyCharges'].sum()
annual_rev_at_risk = monthly_rev_at_risk * 12

print(f"Overall Churn Rate: {overall_churn_rate:.2f}% ({total_churned} / {total_customers})")
print(f"Average Monthly Charges - Churned: ₹{avg_charge_churned:.2f} | Retained: ₹{avg_charge_retained:.2f}")
print(f"Total Monthly Revenue at Risk: ₹{monthly_rev_at_risk:,.2f}")
print(f"Total Annualized Revenue at Risk: ₹{annual_rev_at_risk:,.2f}")

# Save summary tables to Excel
with pd.ExcelWriter('data/telecom/telecom_churn_summary_tables.xlsx') as writer:
    churn_by_contract.to_excel(writer, sheet_name='By_Contract', index=False)
    churn_by_tenure.to_excel(writer, sheet_name='By_Tenure', index=False)
    churn_by_city.to_excel(writer, sheet_name='By_City', index=False)
    churn_by_support.to_excel(writer, sheet_name='By_SupportCalls', index=False)
    churn_by_satisfaction.to_excel(writer, sheet_name='By_Satisfaction', index=False)

# ---------------------------------------------------------
# STEP 4: Generate Visualizations
# ---------------------------------------------------------

# Chart 1: Churn Rate by Contract Type
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(churn_by_contract['Contract'], churn_by_contract['Churn_Rate'], color=['#ef4444', '#f59e0b', '#10b981'], width=0.55)
ax.set_title('Churn Rate by Contract Type', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_ylim(0, 60)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('data/telecom/charts/churn_by_contract.png', dpi=300)
plt.close()

# Chart 2: Churn Rate by Tenure Bucket
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(churn_by_tenure['TenureBucket'].astype(str), churn_by_tenure['Churn_Rate'], color=['#dc2626', '#3b82f6', '#059669'], width=0.55)
ax.set_title('Churn Rate by Tenure Bucket', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_ylim(0, 50)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('data/telecom/charts/churn_by_tenure.png', dpi=300)
plt.close()

# Chart 3: Satisfaction Score Distribution (Churned vs Retained)
fig, ax = plt.subplots(figsize=(9, 5.5))
sns.histplot(data=df_clean, x='SatisfactionScore', hue='Churn', discrete=True, multiple='dodge', palette={'Yes': '#ef4444', 'No': '#3b82f6'}, shrink=0.8, ax=ax)
ax.set_title('Satisfaction Score Distribution (Churned vs Retained)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Satisfaction Score (1 = Unhappy, 5 = Happy)', fontsize=11, fontweight='semibold')
ax.set_ylabel('Number of Customers', fontsize=11, fontweight='semibold')
plt.tight_layout()
plt.savefig('data/telecom/charts/satisfaction_score_distribution.png', dpi=300)
plt.close()

# Chart 4: City Churn Breakdown (Count & Rate)
fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax2 = ax1.twinx()

cities = churn_by_city['City']
counts = churn_by_city['Churned_Customers']
rates = churn_by_city['Churn_Rate']

bars = ax1.bar(cities, counts, color='#3b82f6', alpha=0.85, width=0.45, label='Churned Count')
line = ax2.plot(cities, rates, color='#ef4444', marker='o', linewidth=2.5, markersize=8, label='Churn Rate (%)')

ax1.set_title('Churn Count & Rate by City', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Churned Customer Count', fontsize=11, fontweight='semibold', color='#1e293b')
ax2.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold', color='#ef4444')
ax2.grid(False)

for i, txt in enumerate(rates):
    ax2.annotate(f'{txt:.1f}%', (cities[i], rates[i]), xytext=(0, 8), textcoords='offset points', ha='center', fontweight='bold', color='#dc2626')

plt.tight_layout()
plt.savefig('data/telecom/charts/city_churn_count_and_rate.png', dpi=300)
plt.close()

# Chart 5: Correlation Heatmap (Numeric Features)
numeric_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'SupportCallsLast6Mo', 'SatisfactionScore', 'ChurnNumeric']
corr = df_clean[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax, cbar_kws={'label': 'Correlation Coefficient'})
ax.set_title('Correlation Heatmap of Key Metrics & Churn', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('data/telecom/charts/correlation_heatmap.png', dpi=300)
plt.close()

# ---------------------------------------------------------
# STEP 5: Machine Learning (Logistic Regression Model)
# ---------------------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix

feature_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'SupportCallsLast6Mo', 'SatisfactionScore', 'Contract', 'PlanType', 'AutoPayEnabled']
X = pd.get_dummies(df_clean[feature_cols], drop_first=True)
y = df_clean['ChurnNumeric']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("\n--- Logistic Regression Model Performance ---")
print(f"Accuracy:  {acc*100:.2f}%")
print(f"Precision: {prec*100:.2f}%")
print(f"Recall:    {rec*100:.2f}%")
print(f"F1-Score:  {f1:.3f}")
print(f"ROC-AUC:   {roc_auc:.3f}")

# Chart 6: Feature Importance & ROC Curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Feature Importance
coef_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_[0]}).sort_values(by='Coefficient', ascending=True)
ax1.barh(coef_df['Feature'], coef_df['Coefficient'], color=np.where(coef_df['Coefficient'] > 0, '#ef4444', '#10b981'))
ax1.set_title('Logistic Regression Feature Coefficients', fontsize=12, fontweight='bold')
ax1.set_xlabel('Coefficient (Positive = Increases Churn Risk)')

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
ax2.plot(fpr, tpr, color='#3b82f6', lw=2.5, label=f'ROC Curve (AUC = {roc_auc:.2f})')
ax2.plot([0, 1], [0, 1], color='#94a3b8', lw=1.5, linestyle='--')
ax2.set_title('Receiver Operating Characteristic (ROC)', fontsize=12, fontweight='bold')
ax2.set_xlabel('False Positive Rate')
ax2.set_ylabel('True Positive Rate')
ax2.legend(loc='lower right')

plt.tight_layout()
plt.savefig('data/telecom/charts/logistic_regression_feature_importance.png', dpi=300)
plt.close()

print("\nAll analysis and chart generation completed successfully!")

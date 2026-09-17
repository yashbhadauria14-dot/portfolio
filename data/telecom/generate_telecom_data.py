import numpy as np
import pandas as pd
import os

# Set random seed for reproducible realistic data
np.random.seed(42)

n_samples = 1200

customer_ids = [f"CUST-{1001 + i}" for i in range(n_samples)]
genders = np.random.choice(['Male', 'Female'], size=n_samples, p=[0.51, 0.49])
ages = np.random.randint(18, 76, size=n_samples)

# Inconsistent city casing in raw CRM pull
cities_raw = ['Mumbai', 'mumbai', 'MUMBAI', 'Delhi', 'delhi', 'DELHI', 
              'Bengaluru', 'bengaluru', 'BENGALURU', 'Hyderabad', 'hyderabad', 
              'Chennai', 'chennai', 'Pune', 'pune']
city_probs = [0.10, 0.08, 0.07, 0.12, 0.08, 0.05, 0.12, 0.08, 0.05, 0.08, 0.04, 0.05, 0.03, 0.03, 0.02]
cities = np.random.choice(cities_raw, size=n_samples, p=city_probs)

tenures = np.random.randint(1, 61, size=n_samples)
plan_types = np.random.choice(['Basic', 'Standard', 'Premium'], size=n_samples, p=[0.35, 0.45, 0.20])

contracts = np.random.choice(['Month-to-Month', '1 Year', '2 Year'], size=n_samples, p=[0.55, 0.30, 0.15])
payment_methods = np.random.choice(['UPI', 'Credit Card', 'Net Banking', 'Cash'], size=n_samples, p=[0.40, 0.30, 0.20, 0.10])
support_calls = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=n_samples, p=[0.25, 0.30, 0.20, 0.12, 0.07, 0.04, 0.02])
autopay = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.38, 0.62])
satisfaction_scores = np.random.choice([1.0, 2.0, 3.0, 4.0, 5.0], size=n_samples, p=[0.18, 0.22, 0.25, 0.20, 0.15])

# Calculate monthly charges based on PlanType with slight noise
monthly_charges = []
for plan in plan_types:
    if plan == 'Basic':
        base = np.random.normal(499, 45)
    elif plan == 'Standard':
        base = np.random.normal(899, 65)
    else: # Premium
        base = np.random.normal(1299, 85)
    monthly_charges.append(round(max(299, base), 2))

# Compute churn probability based on realistic business factors
churn_probs = []
for i in range(n_samples):
    p = 0.15 # base churn probability
    
    # Contract impact
    if contracts[i] == 'Month-to-Month':
        p += 0.25
    elif contracts[i] == '1 Year':
        p -= 0.05
    elif contracts[i] == '2 Year':
        p -= 0.12
        
    # Tenure impact (<12 months high risk)
    if tenures[i] < 12:
        p += 0.18
    elif tenures[i] >= 36:
        p -= 0.10
        
    # Support calls impact
    if support_calls[i] >= 3:
        p += 0.25
    elif support_calls[i] == 0:
        p -= 0.05
        
    # Satisfaction score impact
    if satisfaction_scores[i] <= 2.0:
        p += 0.20
    elif satisfaction_scores[i] >= 4.0:
        p -= 0.10
        
    # AutoPay impact
    if autopay[i] == 'No':
        p += 0.08
        
    # Clamp probability between 0.02 and 0.92
    p = max(0.02, min(0.92, p))
    churn_probs.append(p)

churn_outcomes = ['Yes' if np.random.rand() < prob else 'No' for prob in churn_probs]

# Assemble DataFrame
df = pd.DataFrame({
    'CustomerID': customer_ids,
    'Gender': genders,
    'Age': ages,
    'City': cities,
    'TenureMonths': tenures,
    'PlanType': plan_types,
    'MonthlyCharges': monthly_charges,
    'Contract': contracts,
    'PaymentMethod': payment_methods,
    'SupportCallsLast6Mo': support_calls,
    'AutoPayEnabled': autopay,
    'SatisfactionScore': satisfaction_scores,
    'Churn': churn_outcomes
})

# Inject missing values (NaN) to simulate raw CRM export
# ~8% missing in SatisfactionScore
satisfaction_mask = np.random.rand(n_samples) < 0.08
df.loc[satisfaction_mask, 'SatisfactionScore'] = np.nan

# ~5% missing in PaymentMethod
payment_mask = np.random.rand(n_samples) < 0.05
df.loc[payment_mask, 'PaymentMethod'] = np.nan

# Inject duplicate rows (~25 duplicate rows)
duplicates = df.sample(n=25, random_state=42)
df_dirty = pd.concat([df, duplicates], ignore_index=True)

# Shuffle rows
df_dirty = df_dirty.sample(frac=1, random_state=101).reset_index(drop=True)

# Create output directories
os.makedirs('data/telecom', exist_ok=True)
output_path = 'data/telecom/telecom_customer_churn.csv'
df_dirty.to_csv(output_path, index=False)

print(f"Successfully generated dirty dataset '{output_path}' with shape: {df_dirty.shape}")
print(f"Missing SatisfactionScore: {df_dirty['SatisfactionScore'].isnull().sum()}")
print(f"Missing PaymentMethod: {df_dirty['PaymentMethod'].isnull().sum()}")
print(f"Duplicate rows: {df_dirty.duplicated().sum()}")

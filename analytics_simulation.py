
# analytics_simulation.py
# Run this script to simulate rule-based fraud detection and produce outputs in outputs/ folder.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

df = pd.read_json('sample_data/transactions.jsonl', lines=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(['user_id','timestamp']).reset_index(drop=True)

# Rule 1: amount > 15000
df['flag_amount'] = df['amount'] > 15000

# Rule 2: 3+ transactions within 2 minutes for same user
df['txn_count_2min'] = 0
for user in df['user_id'].unique():
    sub = df[df['user_id']==user].copy()
    sub = sub.sort_values('timestamp').reset_index()
    counts = []
    for i in range(len(sub)):
        window_start = sub.loc[i,'timestamp'] - pd.Timedelta(minutes=2)
        cnt = sub[(sub['timestamp'] >= window_start) & (sub['timestamp'] <= sub.loc[i,'timestamp'])].shape[0]
        counts.append(cnt)
    df.loc[sub['index'],'txn_count_2min'] = counts

df['flag_rapid'] = df['txn_count_2min'] >= 3

# Final fraud flag
df['fraud_flag'] = ((df['flag_amount']) | (df['flag_rapid'])).map({True:'POTENTIAL_FRAUD', False:'LEGIT'})

# Save outputs
df.to_csv('outputs/flagged_transactions.csv', index=False)

agg = df.groupby('user_id').agg(
    total_transactions=('txn_id','count'),
    total_amount=('amount','sum'),
    avg_amount=('amount','mean'),
    fraud_count=('fraud_flag', lambda s: (s=='POTENTIAL_FRAUD').sum())
).reset_index()
agg.to_csv('outputs/aggregated_by_user.csv', index=False)

# Plots
import matplotlib.pyplot as plt
plt.figure(figsize=(8,4))
plt.bar(agg['user_id'], agg['avg_amount'])
plt.xlabel('User ID')
plt.ylabel('Average Transaction Amount (INR)')
plt.title('Average Transaction Amount per User')
plt.tight_layout()
plt.savefig('outputs/sample_output.png')
plt.close()

ts = df.set_index('timestamp').resample('1T').apply({'fraud_flag': lambda s: (s=='POTENTIAL_FRAUD').sum()}).rename(columns={'fraud_flag':'fraud_count'})
ts['fraud_count'].fillna(0, inplace=True)
plt.figure(figsize=(10,4))
plt.plot(ts.index, ts['fraud_count'], marker='o')
plt.xlabel('Time')
plt.ylabel('Fraud Count per Minute')
plt.title('Fraud Events Over Time')
plt.tight_layout()
plt.savefig('outputs/fraud_timeseries.png')
plt.close()

print('Generated outputs in outputs/ folder')

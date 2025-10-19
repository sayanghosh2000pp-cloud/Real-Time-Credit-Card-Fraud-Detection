# Real-Time-Credit-Card-Fraud-Detection
Real-Time Credit Card Fraud Detection (Rule-Based)
# Real-Time Credit Card Fraud Detection (Rule-Based)

## Description
This project simulates a **real-time credit card fraud detection system** using rule-based logic. 
It generates synthetic transactions, flags potential fraud based on:
- Transaction amount > ₹15,000
- 3 or more transactions by the same user within 2 minutes

The project demonstrates data engineering and analytics skills using Python, Pandas, Matplotlib, and PySpark.

## Features
- Generates realistic transaction data (`sample_data/transactions.jsonl`)
- Flags potential fraudulent transactions (`outputs/flagged_transactions.csv`)
- Aggregates metrics per user (`outputs/aggregated_by_user.csv`)
- Visualizes results with charts:
    - Average Transaction Amount per User (`outputs/sample_output.png`)
    - Fraud Events Over Time (`outputs/fraud_timeseries.png`)

## Technologies
- Python 3
- Pandas, NumPy, Matplotlib
- PySpark
- Kafka (optional for full streaming)

## How to Run
1. **Run analytics simulation** (no Kafka needed):
```bash
python analytics_simulation.py

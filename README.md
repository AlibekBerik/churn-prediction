\# Customer Churn Prediction — SQL RFM Features + SMOTE



Predicts which e-commerce customers are likely to churn using SQL-derived RFM (Recency, Frequency, Monetary) features and an XGBoost classifier, with a comparison of baseline vs. SMOTE-balanced training to address class imbalance.



\## Problem



Businesses lose revenue when customers quietly stop purchasing. This project identifies at-risk customers from historical transaction data so retention efforts can be targeted before they leave.



\## Dataset



\[Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) (UCI) — 800K+ real e-commerce transactions spanning Dec 2009–Dec 2011, across 5,878 unique customers. Not included in this repo due to size; download it and place it in `data/` to reproduce.



\## Approach



1\. \*\*Data cleaning\*\* (`src/load\_data.py`) — removed cancelled orders, missing customer IDs, and invalid quantity/price values; loaded into a SQLite database.

2\. \*\*SQL feature engineering\*\* (`src/features.sql`) — calculated Recency, Frequency, and Monetary value per customer using CTEs, aggregations, and date functions. Churn label defined as no purchase in 365+ days, chosen after testing multiple thresholds (30/90/180/365 days) to find a realistic, meaningfully imbalanced split.

3\. \*\*Baseline model\*\* (`src/train\_baseline.py`) — XGBoost trained on Frequency and Monetary features. (Recency was deliberately excluded from features since it directly determines the label — including it caused target leakage and a meaningless \~100% AUC-ROC during initial testing.)

4\. \*\*SMOTE-balanced model\*\* (`src/train\_smote.py`) — applied SMOTE to the training set only (never the test set, to avoid data leakage) to address class imbalance.

5\. \*\*Interactive dashboard\*\* (`app.py`) — Streamlit app for looking up any customer's RFM profile and live churn risk score.



\## Results



| Approach | AUC-ROC | Recall (churned) | Precision (churned) |

|---|---|---|---|

| Baseline | 0.754 | 0.40 | 0.52 |

| SMOTE | 0.759 | \*\*0.67\*\* | 0.47 |



SMOTE substantially improved the model's ability to catch actual churners (recall +68% relative improvement), at a modest precision tradeoff — a worthwhile exchange in a churn context, where missing a real churner is typically costlier than a false alarm.



\## How to run locally



```bash

python -m venv venv

venv\\Scripts\\Activate.ps1   # Windows

pip install -r requirements.txt



python src/load\_data.py

python src/build\_features.py

python src/train\_baseline.py

python src/train\_smote.py

streamlit run app.py

```



\## Tech stack



Python, SQLite/SQL, Pandas, XGBoost, imbalanced-learn (SMOTE), Streamlit



\## Live demo



\[Add your Streamlit Cloud link here once deployed]


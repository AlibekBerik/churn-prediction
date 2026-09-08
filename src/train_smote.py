import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib

df = pd.read_csv("data/rfm_features.csv")
X = df[["frequency", "monetary"]]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SMOTE only touches the training data — the test set stays 100% real
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Before SMOTE:", y_train.value_counts().to_dict())
print("After SMOTE:", y_train_resampled.value_counts().to_dict())

model = xgb.XGBClassifier(eval_metric="logloss", random_state=42)
model.fit(X_train_resampled, y_train_resampled)

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
print("AUC-ROC:", roc_auc_score(y_test, probs))

joblib.dump(model, "model.pkl")
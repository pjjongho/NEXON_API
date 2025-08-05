import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib
import os

from model.utils import load_data


# data load
X, y = load_data()

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
    )

# define model
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

# Training
rf.fit(X_train, y_train)

# Predict
y_pred = rf.predict(X_test)

# Evaluation

print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model
os.makedirs("./model/saved_models", exist_ok=True)
joblib.dump(rf, "./model/saved_models/random_forest.pkl")
print("모델이 './model/saved_models/random_forest.pkl'에 저장됨.")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# ----------------------------
# LOAD DATASET
# ----------------------------
df = pd.read_csv("dataset_large.csv")

print("Total samples:", len(df))
print("Label distribution:\n", df["label"].value_counts())

# ----------------------------
# FEATURES & LABEL
# ----------------------------
X = df.drop("label", axis=1)
y = df["label"]

# ----------------------------
# TRAIN TEST SPLIT
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ----------------------------
# TRAIN MODEL
# ----------------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ----------------------------
# EVALUATE
# ----------------------------
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ----------------------------
# SAVE MODEL
# ----------------------------
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved as model.pkl")
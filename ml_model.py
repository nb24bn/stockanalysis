import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# 📥 Load preprocessed dataset
df = pd.read_csv("training_data.csv")

# 🔁 Convert labels to binary format
df['Label'] = df['Label'].map({'Not High Potential': 0, 'High Potential': 1})
df = df[df['Label'].isin([0, 1])]

# 🚫 Drop rows with missing values in required fields
df.dropna(subset=[
    'RSI', 'SMA_20', 'SMA_50',
    'MACD', 'Signal_Line',
    'BB_High', 'BB_Low',
    'ATR', 'Volume_Z',
    'Label'
], inplace=True)

print("✅ Cleaned Data Shape:", df.shape)
print("✅ Label Distribution:\n", df['Label'].value_counts())

# 🧠 Features and Target
features = [
    'RSI', 'SMA_20', 'SMA_50',
    'MACD', 'Signal_Line',
    'BB_High', 'BB_Low',
    'ATR', 'Volume_Z'
]
X = df[features]
y = df['Label']

# 🧪 Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ⚙️ Initialize XGBoost
model = XGBClassifier(
    objective='binary:logistic',
    base_score=0.5,
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    eval_metric='logloss'
)

# 🚀 Train
model.fit(X_train, y_train)

# 📊 Evaluation
y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

print("📌 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 💾 Save model
joblib.dump(model, "stock_predictor.pkl")
print("✅ XGBoost model saved as 'stock_predictor.pkl'")

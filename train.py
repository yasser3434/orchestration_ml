import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
import joblib

def compute_accuracy(y_true, y_pred):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
    }


def save_model(model, file_path):
    joblib.dump(model, file_path)


df = pd.read_csv("data/manufacturing_defect_dataset.csv")
# print(df.columns)

y = df["DefectStatus"]
X = df.drop('DefectStatus', axis=1) 

# Feature selection
selector = SelectKBest(score_func=f_regression, k=5)

X_new = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support(indices=True)]
print("Selected features:", selected_features)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
class_predictions = [1 if pred > 0.5 else 0 for pred in predictions]

accuracy = compute_accuracy(y_test, class_predictions)

print(accuracy)

save_model(model, 'model.pkl')
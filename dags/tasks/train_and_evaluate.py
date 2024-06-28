from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest, f_regression
import pandas as pd
from io import BytesIO
import joblib
import base64

def train_and_evaluate(df_json):
    df = pd.read_json(df_json)
    

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

    accuracy = accuracy_score(y_test, class_predictions)

    print(f"Accuracy : {accuracy}")

    # Serialize the model using joblib and encode as base64
    buffer = BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)
    model_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64 encoded model
    return model_base64
    # return {"model_base64": model_base64, "accuracy": accuracy}
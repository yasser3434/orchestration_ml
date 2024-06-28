from sklearn.feature_selection import SelectKBest, f_regression
import pandas as pd

def process_data(json_str):
    df = pd.read_json(json_str)

    # Process the DataFrame
    y = df["DefectStatus"]
    X = df.drop('DefectStatus', axis=1)

    # Feature selection
    selector = SelectKBest(score_func=f_regression, k=5)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support(indices=True)]
    print("Selected features:", selected_features)

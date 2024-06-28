import streamlit as st
import requests

# Streamlit user interface
st.title("Production Quality Prediction")

st.sidebar.header("Input Parameters")
def get_user_input():
    ProductionVolume = st.sidebar.number_input("Production Volume", min_value=0, max_value=999, value=10, step=1)
    DefectRate = st.sidebar.slider("Defect Rate", min_value=0.0, max_value=4.998529423589416, value=0.05, step=0.01)
    QualityScore = st.sidebar.slider("Quality Score", min_value=0.0, max_value=99.99699307332706, value=7.5, step=0.1)
    MaintenanceHours = st.sidebar.number_input("Maintenance Hours", min_value=0, max_value=23, value=10, step=1)
    StockoutRate = st.sidebar.slider("Stockout Rate", min_value=0.0, max_value=0.0999973867646256, value=0.1, step=0.01)

    data = {
        "ProductionVolume": ProductionVolume,
        "DefectRate": DefectRate,
        "QualityScore": QualityScore,
        "MaintenanceHours": MaintenanceHours,
        "StockoutRate": StockoutRate
    }
    return data

input_data = get_user_input()

if st.button("Predict"):
    # Call the FastAPI prediction endpoint
    response = requests.post("http://fastapi:8000/predict", json=input_data)
    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"Prediction: {prediction}")
    else:
        st.error("Error in prediction request")
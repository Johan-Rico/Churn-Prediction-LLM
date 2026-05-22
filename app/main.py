from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from src.llm import generar_explicacion_churn
from src.model import predict_churn_with_probability


st.set_page_config(
	page_title="Churn Predictor",
	page_icon="📉",
	layout="wide",
)


@st.cache_data
def load_dataset_stats() -> dict[str, float]:
	dataset_path = PROJECT_ROOT / "data" / "telco_clean.csv"
	df = pd.read_csv(dataset_path)
	return {
		"rows": float(df.shape[0]),
		"churn_rate": float((df["Churn"] == "Yes").mean()),
		"avg_tenure": float(df["tenure"].mean()),
		"avg_monthly": float(df["MonthlyCharges"].mean()),
	}


def get_customer_input() -> dict[str, object]:
	st.sidebar.header("Datos del cliente")

	gender = st.sidebar.selectbox("Género", ["Female", "Male"], index=0)
	senior_citizen = st.sidebar.selectbox("Senior citizen", [0, 1], index=0)
	partner = st.sidebar.selectbox("¿Tiene pareja?", ["Yes", "No"], index=1)
	dependents = st.sidebar.selectbox("¿Tiene dependientes?", ["Yes", "No"], index=1)
	tenure = st.sidebar.slider("Meses como cliente", 0, 72, 2)
	phone_service = st.sidebar.selectbox("PhoneService", ["Yes", "No"], index=0)
	multiple_lines = st.sidebar.selectbox("MultipleLines", ["No", "Yes", "No phone service"], index=0)
	internet_service = st.sidebar.selectbox("InternetService", ["DSL", "Fiber optic", "No"], index=1)
	online_security = st.sidebar.selectbox("OnlineSecurity", ["No", "Yes", "No internet service"], index=0)
	online_backup = st.sidebar.selectbox("OnlineBackup", ["No", "Yes", "No internet service"], index=0)
	device_protection = st.sidebar.selectbox("DeviceProtection", ["No", "Yes", "No internet service"], index=0)
	tech_support = st.sidebar.selectbox("TechSupport", ["No", "Yes", "No internet service"], index=0)
	streaming_tv = st.sidebar.selectbox("StreamingTV", ["No", "Yes", "No internet service"], index=0)
	streaming_movies = st.sidebar.selectbox("StreamingMovies", ["No", "Yes", "No internet service"], index=0)
	contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"], index=0)
	paperless_billing = st.sidebar.selectbox("PaperlessBilling", ["Yes", "No"], index=0)
	payment_method = st.sidebar.selectbox(
		"PaymentMethod",
		["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
		index=0,
	)
	monthly_charges = st.sidebar.slider("MonthlyCharges", 18.0, 120.0, 85.5, 0.1)
	total_charges = st.sidebar.number_input("TotalCharges", min_value=0.0, max_value=10000.0, value=171.0, step=1.0)

	return {
		"gender": gender,
		"SeniorCitizen": senior_citizen,
		"Partner": partner,
		"Dependents": dependents,
		"tenure": tenure,
		"PhoneService": phone_service,
		"MultipleLines": multiple_lines,
		"InternetService": internet_service,
		"OnlineSecurity": online_security,
		"OnlineBackup": online_backup,
		"DeviceProtection": device_protection,
		"TechSupport": tech_support,
		"StreamingTV": streaming_tv,
		"StreamingMovies": streaming_movies,
		"Contract": contract,
		"PaperlessBilling": paperless_billing,
		"PaymentMethod": payment_method,
		"MonthlyCharges": monthly_charges,
		"TotalCharges": total_charges,
	}


def main() -> None:
	st.title("Predicción de Churn de Clientes")
	st.write(
		"Ingresa los datos de un cliente y el sistema estimará la probabilidad de abandono y generará una explicación en español con Groq."
	)

	stats = load_dataset_stats()
	col1, col2, col3 = st.columns(3)
	col1.metric("Clientes analizados", f"{int(stats['rows']):,}")
	col2.metric("Tasa de churn", f"{stats['churn_rate']:.1%}")
	col3.metric("Tenure promedio", f"{stats['avg_tenure']:.1f} meses")

	customer_data = get_customer_input()

	if st.button("Predecir churn", type="primary"):
		with st.spinner("Calculando predicción..."):
			result = predict_churn_with_probability(customer_data)

		probability = result["probability"]
		risk_label = result["risk_label"]
		prediction_text = "Abandona" if result["prediction"] == 1 else "No abandona"

		st.subheader("Resultado")
		result_col1, result_col2, result_col3 = st.columns(3)
		result_col1.metric("Clase", prediction_text)
		result_col2.metric("Probabilidad de churn", f"{probability:.1%}")
		result_col3.metric("Nivel de riesgo", risk_label)

		st.info(f"El modelo clasifica a este cliente como: {prediction_text}.")

		with st.spinner("Generando explicación con Groq..."):
			try:
				explanation = generar_explicacion_churn(customer_data, probability)
			except Exception as exc:
				explanation = (
					"No se pudo generar la explicación con Groq porque falta la API key o hubo un error de conexión. "
					f"Error: {exc}"
				)

		st.subheader("Explicación del perfil de riesgo")
		st.write(explanation)

		with st.expander("Ver datos usados por el modelo"):
			st.json(customer_data)


if __name__ == "__main__":
	main()

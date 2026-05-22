"""Carga del modelo de churn y generación de predicciones."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from src.preprocessing import prepare_customer_input


BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "xgb_churn_model.pkl"
FEATURES_PATH = MODELS_DIR / "feature_columns.pkl"


def load_artifacts() -> tuple[Any, list[str]]:
	"""Carga el modelo entrenado y la lista de columnas esperadas."""
	if not MODEL_PATH.exists():
		raise FileNotFoundError(f"No se encontró el modelo en {MODEL_PATH}")
	if not FEATURES_PATH.exists():
		raise FileNotFoundError(f"No se encontró la lista de columnas en {FEATURES_PATH}")

	model = joblib.load(MODEL_PATH)
	feature_columns = joblib.load(FEATURES_PATH)
	return model, feature_columns


def predict_churn(customer_data: dict[str, Any]) -> tuple[int, float]:
	"""Devuelve la clase predicha y la probabilidad de churn."""
	model, feature_columns = load_artifacts()
	prepared_input = prepare_customer_input(customer_data, feature_columns)
	probability = float(model.predict_proba(prepared_input)[0, 1])
	prediction = int(probability >= 0.5)
	return prediction, probability


def predict_churn_with_probability(customer_data: dict[str, Any]) -> dict[str, Any]:
	"""Agrupa la predicción y sus metadatos en un solo diccionario."""
	prediction, probability = predict_churn(customer_data)
	risk_label = "Alto" if probability >= 0.7 else "Medio" if probability >= 0.4 else "Bajo"

	return {
		"prediction": prediction,
		"probability": probability,
		"risk_label": risk_label,
		"risk_class": "Churn" if prediction == 1 else "No Churn",
	}

"""Utilidades para preparar la entrada del formulario antes de predecir churn."""

from __future__ import annotations

from typing import Any

import pandas as pd


def build_customer_frame(customer_data: dict[str, Any]) -> pd.DataFrame:
	"""Convierte un diccionario de cliente en un DataFrame de una fila."""
	frame = pd.DataFrame([customer_data]).copy()

	if "customerID" in frame.columns:
		frame = frame.drop(columns=["customerID"])

	if "TotalCharges" in frame.columns:
		frame["TotalCharges"] = pd.to_numeric(frame["TotalCharges"], errors="coerce").fillna(0)

	if "SeniorCitizen" in frame.columns:
		frame["SeniorCitizen"] = frame["SeniorCitizen"].astype(int)

	return frame


def encode_customer_frame(customer_frame: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
	"""Aplica one-hot encoding y alinea las columnas con el modelo entrenado."""
	encoded = pd.get_dummies(customer_frame, drop_first=True)
	encoded = encoded.reindex(columns=feature_columns, fill_value=0)
	return encoded


def prepare_customer_input(customer_data: dict[str, Any], feature_columns: list[str]) -> pd.DataFrame:
	"""Prepara la entrada completa del cliente para el modelo."""
	customer_frame = build_customer_frame(customer_data)
	return encode_customer_frame(customer_frame, feature_columns)

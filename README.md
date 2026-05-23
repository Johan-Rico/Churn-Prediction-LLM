# Churn Prediction LLM

Sistema de predicción de abandono de clientes (churn) en telecomunicaciones que combina Machine Learning con un LLM que genera explicaciones automáticas en español de cada predicción.

---

## Descripción

El sistema tiene tres capas:

1. **EDA**: Análisis exploratorio del dataset Telco Customer Churn (7,043 clientes, 20 variables). Identifica patrones, desbalance de clases (~26% churn) y variables clave como tenure y tipo de contrato.
2. **Modelo ML**: Baseline con Regresión Logística, Random Forest y XGBoost con GridSearchCV. Evaluados con AUC-ROC y F1. SHAP explica la importancia de cada variable.
3. **LLM integrado**: Groq (Llama 3.1) genera automáticamente un párrafo en español explicando el perfil de riesgo del cliente. Evaluado cuantitativamente con 15 casos de prueba (score 93.3%).

---

## Instalación

### 1. Instalar dependencias

Después de descargar el código instale en terminal las dependencias requeridas:

```
pip install -r requirements.txt
```

### 2. Configurar la API key de Groq

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
GROQ_API_KEY=tu_api_key
```

Obtén tu key gratuita en [console.groq.com](https://console.groq.com).

### 3. Registrar el kernel de Jupyter (solo la primera vez) en Visual Studio Code

```
python -m ipykernel install --user --name python313 --display-name "Python 3.13"
```

---

## Ejecución

### Paso 1 — EDA

Abre y ejecuta todas las celdas de `notebooks/01_eda.ipynb`.

Genera 5 figuras en `data/figures/` y el archivo `data/telco_clean.csv`.

### Paso 2 — Modelado

Abre y ejecuta todas las celdas de `notebooks/02_modeling.ipynb`.

Genera las curvas ROC, la gráfica SHAP y guarda el modelo en `models/`.

### Paso 3 — Probar el LLM

```
python src/llm.py
```

Genera una explicación en español para un cliente de ejemplo con 82% de probabilidad de churn.

### Paso 4 — Ejecutar la app de Streamlit

```
streamlit run app/main.py
```

Abre la interfaz, completa el formulario del cliente y presiona el botón de predicción para ver la probabilidad de churn y la explicación automática.

---

## Estructura del proyecto

```
Churn-Prediction-LLM/
├── notebooks/
│   ├── 01_eda.ipynb                         # EDA con 5 figuras
│   ├── 02_modeling.ipynb                    # Entrenamiento y comparación de modelos
│   └── 03_llm_evaluation.ipynb              # Evaluación cuantitativa del LLM
├── src/
│   ├── llm.py                               # Integración con Groq
│   ├── preprocessing.py                     # Pipeline de preprocesamiento
│   └── model.py                             # Carga del modelo entrenado
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv # Dataset original (Kaggle)
│   ├── telco_clean.csv                      # Dataset limpio (generado)
│   ├── figures/                             # Figuras exportadas (generadas)
│   └── llm_evaluation_results.csv           # Resultados evaluación LLM (generado)
├── models/
│   ├── xgb_churn_model.pkl                  # Modelo XGBoost entrenado (generado)
│   └── feature_columns.pkl                  # Columnas del modelo (generado)
├── app/
│   └── main.py                              # Interfaz Streamlit
├── docs/
│   └── informe_final.pdf                    # Informe LaTeX compilado
├── .env                                     # API key de Groq (NO subir a GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

Los archivos marcados como (generado) se crean al ejecutar los notebooks en orden. No están en el repositorio pero se reproducen en menos de 5 minutos.

---

## Resultados

| Modelo | AUC-ROC | F1 Score |
|--------|---------|----------|
| Regresión Logística (Baseline) | 0.8414 | 0.6164 |
| Random Forest | 0.8433 | 0.6250 |
| XGBoost | 0.8393 | 0.6285 |
| XGBoost (GridSearchCV) | — | — |

Evaluación LLM: 93.3% score promedio sobre 15 casos de prueba con ground truth.

---

## Video demo

[Link al video demo] — Actualizar con el link de YouTube, Drive o Loom

## App desplegada

Puedes probar la app aquí:

https://churn-prediction-ia.streamlit.app/

---

## Integrantes

| Nombre | Correo |
|--------|--------|
| Kadiha Nahir Muhamad Orta | knmuhamado@eafit.edu.co |
| Laura Restrepo Berrío | lrestrepb1@eafit.edu.co |
| Johan Samuel Rico Nivia | jsricon@eafit.edu.co |

---

## Notas
- Ejecutar los notebooks en orden: `01` → `02` → `03`.
- Python 3.13 requerido.
## Instalación
 
 
### 1. Instalar dependencias
 
Después de decargar el código instale en terminal las dependencias requeridas

```bash
pip install -r requirements.txt
```
 
### 2. Configurar la API key de Groq
 
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
 
```
GROQ_API_KEY=tu_api_key
```
 
Obtén tu key gratuita en [console.groq.com](https://console.groq.com).
 
### 3. Registrar el kernel de Jupyter (solo la primera vez) en Visual Studio Code
 
```bash
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
 
```bash
python src/llm.py
```
 
Genera una explicación en español para un cliente de ejemplo con 82% de probabilidad de churn.

### Paso 4 — Ejecutar la app de Streamlit

```bash
streamlit run app/main.py
```

Abre la interfaz, completa el formulario del cliente y presiona el botón de predicción para ver la probabilidad de churn y la explicación automática.
 
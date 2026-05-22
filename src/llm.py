#Módulo de integración con Groq para generar explicaciones en lenguaje natural de las predicciones del modelo de churn.

from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "No se encontró GROQ_API_KEY. "
            "Agrégala como variable de entorno o en un archivo .env"
        )
    return Groq(api_key=api_key)


def generar_explicacion_churn(datos_cliente: dict, probabilidad: float) -> str:
    """
    Genera una explicación en español del perfil de riesgo de un cliente.

    Parámetros:
        datos_cliente: diccionario con las características del cliente
                       (tenure, Contract, MonthlyCharges, etc.)
        probabilidad:  probabilidad de churn predicha por el modelo (0 a 1)

    Retorna:
        Texto con la explicación generada por el LLM.
    """

    # Determinar nivel de riesgo según la probabilidad
    if probabilidad >= 0.7:
        nivel_riesgo = "ALTO"
    elif probabilidad >= 0.4:
        nivel_riesgo = "MEDIO"
    else:
        nivel_riesgo = "BAJO"

    # Construir el prompt con los datos del cliente como contexto
    # El prompt incluye los datos más relevantes identificados en el EDA:
    # tenure, tipo de contrato, cargo mensual e internet
    prompt = f"""Eres un analista de retención de clientes de una empresa de telecomunicaciones.
El modelo de machine learning predijo que el siguiente cliente tiene una probabilidad de abandono (churn) de {probabilidad:.1%}, lo que representa un riesgo {nivel_riesgo}.

Datos del cliente:
- Meses como cliente (tenure): {datos_cliente.get('tenure', 'N/A')}
- Tipo de contrato: {datos_cliente.get('Contract', 'N/A')}
- Cargo mensual: ${datos_cliente.get('MonthlyCharges', 'N/A')}
- Tipo de internet: {datos_cliente.get('InternetService', 'N/A')}
- Soporte técnico: {datos_cliente.get('TechSupport', 'N/A')}
- Facturación sin papel: {datos_cliente.get('PaperlessBilling', 'N/A')}
- Método de pago: {datos_cliente.get('PaymentMethod', 'N/A')}
- Tiene pareja: {datos_cliente.get('Partner', 'N/A')}
- Tiene dependientes: {datos_cliente.get('Dependents', 'N/A')}

Escribe un párrafo breve (máximo 5 oraciones) en español explicando:
1. Por qué este cliente tiene ese nivel de riesgo según sus características
2. Qué factores son los más determinantes
3. Una recomendación concreta de retención

Escribe de forma clara y directa, sin usar términos técnicos de machine learning."""

    client = get_client()

    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Eres un analista experto en retención de clientes. Escribes explicaciones claras y accionables en español."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=300
    )

    return respuesta.choices[0].message.content


if __name__ == "__main__":
    # Prueba rápida del módulo con un cliente de ejemplo
    cliente_ejemplo = {
        "tenure": 2,
        "Contract": "Month-to-month",
        "MonthlyCharges": 85.5,
        "InternetService": "Fiber optic",
        "TechSupport": "No",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "Partner": "No",
        "Dependents": "No"
    }

    probabilidad_ejemplo = 0.82

    print("=== Prueba del módulo LLM ===")
    print(f"Cliente: {cliente_ejemplo}")
    print(f"Probabilidad de churn: {probabilidad_ejemplo:.1%}")
    print()
    print("Explicación generada:")
    print("-" * 50)

    explicacion = generar_explicacion_churn(cliente_ejemplo, probabilidad_ejemplo)
    print(explicacion)
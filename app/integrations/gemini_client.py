"""
Cliente Gemini — RF02, RNF02
Encapsula la llamada HTTPS a la API de Gemini para generar pronósticos de demanda.
La clave se lee exclusivamente desde el Módulo de Configuración (nunca en código fuente).
"""
import re
from typing import List

import google.generativeai as genai

from app.config import settings
from app.repositories.historicos_repo import DatoHistorico

# Inicializar el cliente con la clave del entorno (RNF02)
genai.configure(api_key=settings.GEMINI_API_KEY)

_MODEL_NAME = "gemini-1.5-flash"


class GeminiNoDisponibleError(Exception):
    """La API de Gemini no está disponible o no respondió correctamente."""


class RespuestaGeminiInvalidaError(Exception):
    """La respuesta de Gemini no contiene un entero no negativo válido."""


def generar_pronostico(
    nombre_producto: str,
    periodo_objetivo: str,
    historicos: List[DatoHistorico],
) -> int:
    """
    Invoca la API de Gemini con los datos históricos y retorna la demanda estimada
    como entero no negativo.

    Lanza GeminiNoDisponibleError si hay error de conexión o timeout.
    Lanza RespuestaGeminiInvalidaError si la respuesta no es un entero >= 0.
    """
    # Construir el contexto histórico para el prompt
    historico_texto = "\n".join(
        f"  - Periodo {h.periodo}: {h.demanda_real} unidades"
        for h in historicos
    )

    prompt = (
        f"Eres un modelo de predicción de demanda para supermercados.\n"
        f"Producto: {nombre_producto}\n"
        f"Datos históricos de demanda semanal (formato AAAA-WNN):\n"
        f"{historico_texto}\n\n"
        f"Tarea: Estima la demanda para el periodo {periodo_objetivo}.\n"
        f"Responde ÚNICAMENTE con un número entero no negativo que represente "
        f"las unidades estimadas. No incluyas texto, símbolos, ni explicaciones. "
        f"Solo el número entero."
    )

    try:
        model = genai.GenerativeModel(_MODEL_NAME)
        response = model.generate_content(prompt)
        texto = response.text.strip()
    except Exception as exc:
        raise GeminiNoDisponibleError(
            "El servicio de predicción no está disponible en este momento. "
            "Verifique la conexión y la clave de la API de Gemini."
        ) from exc

    # Extraer el primer entero de la respuesta (robusto ante espacios o texto extra)
    match = re.search(r"\b(\d+)\b", texto)
    if not match:
        raise RespuestaGeminiInvalidaError(
            f"La respuesta de Gemini no contiene un número entero válido: '{texto}'"
        )

    valor = int(match.group(1))
    if valor < 0:
        raise RespuestaGeminiInvalidaError(
            f"La demanda estimada no puede ser negativa. Valor recibido: {valor}"
        )

    return valor

"""
Módulo de Configuración — RNF02
Lee todas las variables de entorno requeridas al inicio.
Si GEMINI_API_KEY no está definida o está vacía, el proceso falla inmediatamente.
"""
import os
import sys
from dotenv import load_dotenv

# Carga el archivo .env si existe (solo para desarrollo local)
load_dotenv()


def _require_env(key: str) -> str:
    """Lee una variable de entorno obligatoria; aborta el proceso si está ausente o vacía."""
    value = os.getenv(key, "").strip()
    if not value:
        print(
            f"ERROR: La variable de entorno '{key}' no está definida o su valor es vacío. "
            "Configure el archivo .env o el entorno de ejecución antes de iniciar el servicio.",
            file=sys.stderr,
        )
        sys.exit(1)
    return value


def _optional_env(key: str, default: str) -> str:
    """Lee una variable de entorno opcional; usa el valor por defecto si no está definida."""
    return os.getenv(key, default).strip() or default


# ── Variables obligatorias ────────────────────────────────────────────────────
GEMINI_API_KEY: str = _require_env("GEMINI_API_KEY")

# ── Variables con valores por defecto ─────────────────────────────────────────
DATABASE_PATH: str = _optional_env("DATABASE_PATH", "database/prediccion_demanda.db")
MCP_BASE_URL: str  = _optional_env("MCP_BASE_URL",  "http://localhost:8001")

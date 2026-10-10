"""
Servicio de Métricas — RF05
Calcula MAE y MAPE sobre los pares comparables disponibles.
- MAE: promedio de diferencias absolutas, 4 decimales.
- MAPE: excluye pares con demanda_real == 0, notifica cantidad excluida, 4 decimales.
"""
from dataclasses import dataclass

from app.repositories.metricas_repo import obtener_pares_comparables


class SinDatosComparablesError(Exception):
    """No existen pares (prediccion, dato_historico) comparables para calcular métricas."""


@dataclass
class ResultadoMetricas:
    mae:                 float  # 4 decimales, unidades de demanda
    mape:                float  # 4 decimales, porcentaje (%)
    pares_utilizados:    int
    pares_excluidos_mape: int   # pares con demanda_real == 0 excluidos del MAPE


def calcular_metricas() -> ResultadoMetricas:
    """
    Calcula MAE y MAPE usando todos los pares comparables disponibles.

    MAE  = sum(|p - r|) / n                          — todos los pares
    MAPE = sum(|p - r| / r) * 100 / n_validos        — excluye r == 0

    Lanza SinDatosComparablesError si no hay pares comparables.
    """
    pares = obtener_pares_comparables()

    if not pares:
        raise SinDatosComparablesError(
            "No existen pares de predicción y dato histórico comparables. "
            "Genere al menos una predicción para un periodo que ya tenga dato histórico."
        )

    n = len(pares)

    # ── MAE ───────────────────────────────────────────────────────────────────
    suma_errores_absolutos = sum(
        abs(par.demanda_estimada - par.demanda_real) for par in pares
    )
    mae = round(suma_errores_absolutos / n, 4)

    # ── MAPE ─────────────────────────────────────────────────────────────────
    pares_validos_mape = [p for p in pares if p.demanda_real != 0]
    pares_excluidos    = n - len(pares_validos_mape)

    if pares_validos_mape:
        suma_mape = sum(
            abs(p.demanda_estimada - p.demanda_real) / p.demanda_real
            for p in pares_validos_mape
        )
        mape = round((suma_mape / len(pares_validos_mape)) * 100, 4)
    else:
        # Todos los datos reales son cero; MAPE no calculable
        mape = 0.0

    return ResultadoMetricas(
        mae=mae,
        mape=mape,
        pares_utilizados=n,
        pares_excluidos_mape=pares_excluidos,
    )

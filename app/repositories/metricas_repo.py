"""
Repositorio de Métricas — RF05
Obtiene todos los pares (prediccion, dato_historico) comparables desde SQLite.
Solo usa datos que tengan tanto predicción como histórico para el mismo producto y periodo.
"""
import sqlite3
from dataclasses import dataclass
from typing import List

from app.config import settings


@dataclass
class ParComparable:
    id_producto:      int
    nombre_producto:  str
    periodo:          str
    demanda_estimada: int
    demanda_real:     int


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def obtener_pares_comparables() -> List[ParComparable]:
    """
    Retorna todos los pares para los que existe tanto predicción
    como dato histórico del mismo id_producto y periodo.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                pr.id_producto,
                p.nombre       AS nombre_producto,
                pr.periodo,
                pr.demanda_estimada,
                dh.demanda_real
            FROM prediccion pr
            JOIN dato_historico dh
              ON dh.id_producto = pr.id_producto
             AND dh.periodo     = pr.periodo
            JOIN producto p ON p.id_producto = pr.id_producto
            ORDER BY pr.periodo ASC
            """
        )
        return [
            ParComparable(
                id_producto=row["id_producto"],
                nombre_producto=row["nombre_producto"],
                periodo=row["periodo"],
                demanda_estimada=row["demanda_estimada"],
                demanda_real=row["demanda_real"],
            )
            for row in cur.fetchall()
        ]
    finally:
        conn.close()

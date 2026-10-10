"""
Script de inicialización de la base de datos SQLite.
Crea las tablas según schema.sql y puebla con datos simulados.
Ejecutar: python database/init_db.py
"""
import os
import sqlite3
from pathlib import Path

BASE_DIR  = Path(__file__).parent
SCHEMA    = BASE_DIR / "schema.sql"
DB_PATH   = BASE_DIR / "prediccion_demanda.db"


# ── Datos simulados ────────────────────────────────────────────────────────────
CATEGORIAS = [
    (1, "Frutas",    "Frutas frescas de temporada"),
    (2, "Verduras",  "Verduras y hortalizas frescas"),
    (3, "Lácteos",   "Productos lácteos ultrafrescos"),
    (4, "Carnes",    "Carnes frescas y refrigeradas"),
    (5, "Panadería", "Pan y productos de panadería diaria"),
]

PRODUCTOS = [
    (1, 1, "Mango",              "kg"),
    (2, 1, "Plátano de seda",    "kg"),
    (3, 2, "Tomate",             "kg"),
    (4, 2, "Lechuga",            "unidad"),
    (5, 3, "Yogurt natural",     "unidad"),
    (6, 4, "Pollo entero",       "kg"),
    (7, 5, "Pan francés",        "unidad"),
]

# 10 semanas de históricos por producto (2024-W01 … 2024-W10)
# Demandas simuladas realistas por producto
HISTORICOS_BASE = {
    1: [320, 298, 345, 310, 330, 355, 342, 328, 315, 360],  # Mango
    2: [480, 510, 495, 520, 488, 503, 515, 499, 525, 540],  # Plátano
    3: [210, 225, 198, 215, 230, 205, 220, 235, 212, 228],  # Tomate
    4: [150, 162, 145, 158, 170, 155, 148, 165, 172, 160],  # Lechuga
    5: [380, 395, 410, 388, 402, 415, 390, 405, 420, 398],  # Yogurt
    6: [290, 305, 288, 310, 298, 315, 302, 295, 308, 320],  # Pollo
    7: [620, 645, 610, 638, 655, 628, 641, 617, 650, 663],  # Pan
}

SEMANAS = [
    "2024-W01", "2024-W02", "2024-W03", "2024-W04", "2024-W05",
    "2024-W06", "2024-W07", "2024-W08", "2024-W09", "2024-W10",
]


def init_db() -> None:
    # Eliminar la BD anterior si existe (idempotente para desarrollo)
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Base de datos anterior eliminada: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # Ejecutar el schema
    schema_sql = SCHEMA.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    print("Schema aplicado.")

    # Insertar categorías
    cur.executemany(
        "INSERT INTO categoria_producto (id_categoria, nombre, descripcion) VALUES (?, ?, ?)",
        CATEGORIAS,
    )

    # Insertar productos
    cur.executemany(
        "INSERT INTO producto (id_producto, id_categoria, nombre, unidad_medida) VALUES (?, ?, ?, ?)",
        PRODUCTOS,
    )

    # Insertar históricos
    historicos_rows = []
    for id_producto, demandas in HISTORICOS_BASE.items():
        for semana, demanda in zip(SEMANAS, demandas):
            historicos_rows.append((id_producto, semana, demanda))

    cur.executemany(
        "INSERT INTO dato_historico (id_producto, periodo, demanda_real) VALUES (?, ?, ?)",
        historicos_rows,
    )

    conn.commit()
    conn.close()

    total_historicos = sum(len(v) for v in HISTORICOS_BASE.values())
    print(
        f"Base de datos inicializada en: {DB_PATH}\n"
        f"  Categorías : {len(CATEGORIAS)}\n"
        f"  Productos  : {len(PRODUCTOS)}\n"
        f"  Históricos : {total_historicos}\n"
    )


if __name__ == "__main__":
    init_db()

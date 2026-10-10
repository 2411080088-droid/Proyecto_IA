-- Schema SQLite para el sistema de predicción de demanda de productos frescos
-- Supermercados Peruanos S.A. — Datos simulados, sin información personal real

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categoria_producto (
    id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre         TEXT    NOT NULL UNIQUE,
    descripcion    TEXT
);

CREATE TABLE IF NOT EXISTS producto (
    id_producto    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria   INTEGER NOT NULL,
    nombre         TEXT    NOT NULL,
    unidad_medida  TEXT    NOT NULL DEFAULT 'unidad',
    activo         INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    FOREIGN KEY (id_categoria) REFERENCES categoria_producto(id_categoria)
);

CREATE INDEX IF NOT EXISTS idx_producto_categoria ON producto(id_categoria);
CREATE INDEX IF NOT EXISTS idx_producto_nombre    ON producto(nombre);

-- El periodo se almacena como texto en formato AAAA-WNN (ej. 2024-W01)
-- Esta representación permite ordenamiento lexicográfico correcto como valor ordinal comparable
CREATE TABLE IF NOT EXISTS dato_historico (
    id_dato_historico  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto        INTEGER NOT NULL,
    periodo            TEXT    NOT NULL,           -- formato AAAA-WNN
    demanda_real       INTEGER NOT NULL CHECK (demanda_real >= 0),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    UNIQUE (id_producto, periodo)
);

CREATE INDEX IF NOT EXISTS idx_historico_producto ON dato_historico(id_producto);
CREATE INDEX IF NOT EXISTS idx_historico_periodo  ON dato_historico(periodo);

CREATE TABLE IF NOT EXISTS prediccion (
    id_prediccion      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto        INTEGER NOT NULL,
    periodo            TEXT    NOT NULL,           -- formato AAAA-WNN
    demanda_estimada   INTEGER NOT NULL CHECK (demanda_estimada >= 0),
    fecha_generacion   TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    UNIQUE (id_producto, periodo)
);

CREATE INDEX IF NOT EXISTS idx_prediccion_producto ON prediccion(id_producto);
CREATE INDEX IF NOT EXISTS idx_prediccion_periodo  ON prediccion(periodo);

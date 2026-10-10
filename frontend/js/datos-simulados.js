/**
 * datos-simulados.js
 * Datos de prueba para el maquetado (B5).
 * No hay lógica de negocio ni conexión a base de datos.
 */

const PRODUCTOS = [
  { id: 1, nombre: 'Lechuga hidropónica', categoria: 'Verduras', unidad: 'unidad' },
  { id: 2, nombre: 'Tomate cherry',        categoria: 'Verduras', unidad: 'kg'     },
  { id: 3, nombre: 'Pechuga de pollo',     categoria: 'Carnes',   unidad: 'kg'     },
  { id: 4, nombre: 'Yogur natural',        categoria: 'Lácteos',  unidad: 'unidad' },
  { id: 5, nombre: 'Fresa fresca',         categoria: 'Frutas',   unidad: 'kg'     },
];

const HISTORICOS = {
  1: [
    { fecha: '2024-10-07', demanda: 312 },
    { fecha: '2024-10-14', demanda: 295 },
    { fecha: '2024-10-21', demanda: 330 },
    { fecha: '2024-10-28', demanda: 318 },
    { fecha: '2024-11-04', demanda: 342 },
    { fecha: '2024-11-11', demanda: 360 },
  ],
  2: [
    { fecha: '2024-10-07', demanda: 88  },
    { fecha: '2024-10-14', demanda: 95  },
    { fecha: '2024-10-21', demanda: 102 },
    { fecha: '2024-10-28', demanda: 91  },
    { fecha: '2024-11-04', demanda: 110 },
    { fecha: '2024-11-11', demanda: 98  },
  ],
  3: [
    { fecha: '2024-10-07', demanda: 540 },
    { fecha: '2024-10-14', demanda: 572 },
    { fecha: '2024-10-21', demanda: 558 },
    { fecha: '2024-10-28', demanda: 601 },
    { fecha: '2024-11-04', demanda: 589 },
    { fecha: '2024-11-11', demanda: 615 },
  ],
  4: [
    { fecha: '2024-10-07', demanda: 210 },
    { fecha: '2024-10-14', demanda: 198 },
    { fecha: '2024-10-21', demanda: 225 },
    { fecha: '2024-10-28', demanda: 217 },
  ],
  5: [
    { fecha: '2024-10-07', demanda: 74  },
    { fecha: '2024-10-14', demanda: 68  },
    { fecha: '2024-10-21', demanda: 81  },
  ],
};

const SEMANAS_DISPONIBLES = [
  { valor: '2024-W47', etiqueta: 'Semana 47 — 2024 (18 nov)' },
  { valor: '2024-W48', etiqueta: 'Semana 48 — 2024 (25 nov)' },
  { valor: '2024-W49', etiqueta: 'Semana 49 — 2024 (02 dic)' },
  { valor: '2024-W50', etiqueta: 'Semana 50 — 2024 (09 dic)' },
];

/* Predicciones ya generadas (para Vista 2) */
const PREDICCIONES = [
  { id: 1, producto: 'Lechuga hidropónica', periodo: '2024-W47', estimado: 355, generada: '2024-11-15 09:12' },
  { id: 2, producto: 'Tomate cherry',       periodo: '2024-W47', estimado: 105, generada: '2024-11-15 09:14' },
  { id: 3, producto: 'Pechuga de pollo',    periodo: '2024-W47', estimado: 628, generada: '2024-11-15 09:15' },
  { id: 4, producto: 'Yogur natural',       periodo: '2024-W47', estimado: 231, generada: '2024-11-15 09:17' },
  { id: 5, producto: 'Lechuga hidropónica', periodo: '2024-W48', estimado: 362, generada: '2024-11-18 10:02' },
  { id: 6, producto: 'Tomate cherry',       periodo: '2024-W48', estimado: 112, generada: '2024-11-18 10:04' },
  { id: 7, producto: 'Pechuga de pollo',    periodo: '2024-W48', estimado: 640, generada: '2024-11-18 10:05' },
];

/* Comparaciones reales vs. pronosticadas (para métricas) */
const COMPARACIONES = [
  { producto: 'Lechuga hidropónica', periodo: '2024-W47', estimado: 355, real: 360, diferencia: 5  },
  { producto: 'Tomate cherry',       periodo: '2024-W47', estimado: 105, real: 98,  diferencia: 7  },
  { producto: 'Pechuga de pollo',    periodo: '2024-W47', estimado: 628, real: 615, diferencia: 13 },
  { producto: 'Yogur natural',       periodo: '2024-W47', estimado: 231, real: 217, diferencia: 14 },
];

/* MAE y MAPE pre-calculados (simulados) */
const METRICAS = {
  mae:             9.75,
  mape:            3.6214,
  pares_usados:    4,
  pares_excluidos: 0,
};

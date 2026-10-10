/**
 * predicciones.js — RF02 (módulo independiente de predicción)
 * Usado si se requiere la lógica de predicción en una página separada.
 * La funcionalidad principal está integrada en historicos.js para index.html.
 */

const API_BASE_PRED = 'http://localhost:8000';

async function generarPrediccionStandalone(productoId, periodo) {
  const resp = await fetch(`${API_BASE_PRED}/predicciones`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ producto_id: parseInt(productoId, 10), periodo }),
    signal: AbortSignal.timeout(30000),
  });
  return { status: resp.status, data: await resp.json() };
}

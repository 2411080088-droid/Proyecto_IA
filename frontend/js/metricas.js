/**
 * metricas.js — RF05
 * Módulo independiente para la consulta y visualización de métricas MAE/MAPE.
 * La funcionalidad principal está integrada en resultados.js para resultados.html.
 */

const API_BASE_MET = 'http://localhost:8000';

async function obtenerMetricas() {
  const resp = await fetch(`${API_BASE_MET}/metricas`,
    { signal: AbortSignal.timeout(5000) });
  return { status: resp.status, data: await resp.json() };
}

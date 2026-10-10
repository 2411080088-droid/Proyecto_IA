/**
 * resultados.js — RF03 y RF05
 * Conecta con el backend FastAPI.
 * GET /predicciones → RF03
 * GET /metricas     → RF05
 */

const API_BASE = 'http://localhost:8000';
const TIMEOUT_MS = 5000;

/* ── RF03: Cargar tabla de predicciones ──────────────────── */
async function cargarPredicciones() {
  const tbody    = document.getElementById('cuerpo-tabla-pred');
  const btnReint = document.getElementById('btn-reintentar-pred');

  tbody.innerHTML = `
    <tr>
      <td colspan="4" class="tabla--vacia">
        <span class="spinner" style="border-color:rgba(0,0,0,.15);border-top-color:#1a6e3c;"></span>
        Cargando predicciones…
      </td>
    </tr>`;
  btnReint.classList.add('oculto');

  const inicio = Date.now();

  try {
    const resp = await fetch(`${API_BASE}/predicciones`,
      { signal: AbortSignal.timeout(TIMEOUT_MS) });

    /* RF03-CA5: verificar tiempo */
    if (Date.now() - inicio > TIMEOUT_MS) {
      throw new Error('timeout');
    }

    const data = await resp.json();

    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}`);
    }

    const predicciones = data.predicciones || [];

    /* RF03-CA3: sin predicciones */
    if (!predicciones.length) {
      tbody.innerHTML = `
        <tr><td colspan="4" class="tabla--vacia">
          ${data.mensaje || 'Aún no se han generado predicciones.'}
        </td></tr>`;
      document.getElementById('conteo-predicciones').textContent = '';
      return;
    }

    /* RF03-CA2: ya vienen ordenadas por periodo ASC desde el backend */
    tbody.innerHTML = '';
    predicciones.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.nombre_producto}</td>
        <td><span class="badge badge--azul">${p.periodo}</span></td>
        <td class="texto-der negrita">${Number(p.cantidad_estimada).toLocaleString('es-PE')}</td>
        <td class="texto-centro" style="font-size:.8rem;color:#546e7a">${p.fecha_generacion || '—'}</td>`;
      tbody.appendChild(tr);
    });

    document.getElementById('conteo-predicciones').textContent =
      `${predicciones.length} registro${predicciones.length !== 1 ? 's' : ''}`;

  } catch (err) {
    const esTimeout = err.name === 'TimeoutError' || err.name === 'AbortError' || err.message === 'timeout';
    tbody.innerHTML = `
      <tr><td colspan="4" class="tabla--vacia" style="color:#c62828">
        ${esTimeout
          ? 'La carga tardó demasiado. Intente nuevamente.'
          : 'No se pudo conectar con el servidor. Verifique que el backend esté en ejecución.'}
      </td></tr>`;
    btnReint.classList.remove('oculto');
  }
}

/* ── RF05: Cargar métricas ───────────────────────────────── */
async function cargarMetricas() {
  const seccion  = document.getElementById('seccion-metricas');
  const btnReint = document.getElementById('btn-reintentar-met');
  const alerta   = document.getElementById('alerta-metricas');

  alerta.className = 'alerta alerta--oculta';
  btnReint.classList.add('oculto');
  ['kpi-mae', 'kpi-mape', 'kpi-pares'].forEach(id => {
    document.getElementById(id).textContent = '…';
  });

  try {
    const resp = await fetch(`${API_BASE}/metricas`,
      { signal: AbortSignal.timeout(TIMEOUT_MS) });
    const data = await resp.json();

    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

    /* RF05-CA3: sin datos comparables */
    if (!data.mae || data.mae === null) {
      alerta.className = 'alerta alerta--aviso';
      alerta.textContent = data.mensaje ||
        'No es posible calcular métricas: no existen pares de predicción y dato histórico comparables.';
      seccion.classList.add('oculto');
      return;
    }

    /* RF05-CA1 y CA4: mostrar MAE, MAPE con 4 decimales y unidades */
    document.getElementById('kpi-mae').textContent  = Number(data.mae.valor).toFixed(4);
    document.getElementById('kpi-mape').textContent = Number(data.mape.valor).toFixed(4);
    document.getElementById('kpi-pares').textContent = data.pares_utilizados;

    /* RF05-CA6: pares excluidos del MAPE */
    const alertaExcl = document.getElementById('alerta-excluidos');
    if (data.pares_excluidos_mape > 0) {
      alertaExcl.className = 'alerta alerta--aviso';
      alertaExcl.textContent = data.nota_mape ||
        `Se excluyeron ${data.pares_excluidos_mape} par(es) del cálculo del MAPE porque el valor real era cero.`;
    } else {
      alertaExcl.className = 'alerta alerta--oculta';
    }

    /* Tabla de comparaciones (mismos pares que usaron las métricas) */
    await cargarTablaComparaciones();

    seccion.classList.remove('oculto');

  } catch (err) {
    const esTimeout = err.name === 'TimeoutError' || err.name === 'AbortError';
    alerta.className = 'alerta alerta--error';
    alerta.textContent = esTimeout
      ? 'El cálculo de métricas tardó demasiado. Intente nuevamente.'
      : 'No se pudo obtener las métricas. Verifique que el backend esté en ejecución.';
    btnReint.classList.remove('oculto');
    seccion.classList.add('oculto');
  }
}

/* ── Tabla de comparaciones integrada ───────────────────── */
async function cargarTablaComparaciones() {
  const tbody = document.getElementById('cuerpo-tabla-comp');
  tbody.innerHTML = `<tr><td colspan="5" class="tabla--vacia">Cargando comparaciones…</td></tr>`;

  try {
    /* Obtenemos predicciones para luego comparar cada una */
    const resp = await fetch(`${API_BASE}/predicciones`,
      { signal: AbortSignal.timeout(TIMEOUT_MS) });
    const data = await resp.json();
    const predicciones = data.predicciones || [];

    if (!predicciones.length) {
      tbody.innerHTML = `<tr><td colspan="5" class="tabla--vacia">Sin datos de comparación disponibles.</td></tr>`;
      return;
    }

    /* Consultar comparaciones en paralelo (máx 10 para no saturar) */
    const lote = predicciones.slice(0, 10);
    const resultados = await Promise.allSettled(
      lote.map(p =>
        fetch(`${API_BASE}/comparacion?producto_id=${p.id_producto || ''}&periodo=${p.periodo}`,
          { signal: AbortSignal.timeout(TIMEOUT_MS) }).then(r => r.json())
      )
    );

    tbody.innerHTML = '';
    let hayFilas = false;
    resultados.forEach(r => {
      if (r.status !== 'fulfilled') return;
      const c = r.value;
      if (c.prediccion == null || c.dato_historico == null) return;
      hayFilas = true;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${c.nombre_producto}</td>
        <td><span class="badge badge--azul">${c.periodo}</span></td>
        <td class="texto-der">${Number(c.dato_historico).toLocaleString('es-PE')}</td>
        <td class="texto-der">${Number(c.prediccion).toLocaleString('es-PE')}</td>
        <td class="texto-der negrita">${Number(c.diferencia_absoluta).toLocaleString('es-PE')}</td>`;
      tbody.appendChild(tr);
    });

    if (!hayFilas) {
      tbody.innerHTML = `<tr><td colspan="5" class="tabla--vacia">No hay pares comparables disponibles aún.</td></tr>`;
    }
  } catch {
    tbody.innerHTML = `<tr><td colspan="5" class="tabla--vacia">No se pudieron cargar las comparaciones.</td></tr>`;
  }
}

/* ── Bootstrap ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  cargarPredicciones();
  cargarMetricas();

  document.getElementById('btn-reintentar-pred')
    .addEventListener('click', cargarPredicciones);

  document.getElementById('btn-reintentar-met')
    .addEventListener('click', cargarMetricas);
});

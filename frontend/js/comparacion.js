/**
 * comparacion.js — RF04
 * Compara la demanda pronosticada con la demanda real para un producto y periodo.
 * GET /comparacion?producto_id=X&periodo=AAAA-WNN
 */

const API_BASE_COMP = 'http://localhost:8000';

function mostrarAlertaComp(tipo, mensaje) {
  const el = document.getElementById('alerta-comparacion');
  if (!el) return;
  el.className = `alerta alerta--${tipo}`;
  el.textContent = mensaje;
}

function ocultarAlertaComp() {
  const el = document.getElementById('alerta-comparacion');
  if (el) el.className = 'alerta alerta--oculta';
}

async function consultarComparacion(productoId, periodo) {
  if (!productoId || !periodo) {
    mostrarAlertaComp('aviso', 'Seleccione un producto y un periodo.');
    return;
  }

  const seccion = document.getElementById('seccion-comparacion');
  const btn     = document.getElementById('btn-comparar');
  if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Comparando…'; }
  ocultarAlertaComp();

  try {
    const resp = await fetch(
      `${API_BASE_COMP}/comparacion?producto_id=${productoId}&periodo=${encodeURIComponent(periodo)}`,
      { signal: AbortSignal.timeout(5000) }
    );
    const data = await resp.json();

    if (resp.status === 404) {
      mostrarAlertaComp('error', data.detalle || 'Producto no encontrado.');
      if (seccion) seccion.classList.add('oculto');
      return;
    }

    if (resp.status === 503) {
      mostrarAlertaComp('error',
        (data.detalle || 'Servidor no disponible.') + ' — ' + (data.reintento || ''));
      if (seccion) seccion.classList.add('oculto');
      return;
    }

    /* Mostrar el resultado */
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val !== null && val !== undefined
        ? Number(val).toLocaleString('es-PE')
        : '—';
    };

    setVal('comp-prediccion',   data.prediccion);
    setVal('comp-dato-real',    data.dato_historico);
    setVal('comp-diferencia',   data.diferencia_absoluta);

    const elProd = document.getElementById('comp-producto');
    if (elProd) elProd.textContent = data.nombre_producto;
    const elPer = document.getElementById('comp-periodo');
    if (elPer) elPer.textContent = data.periodo;

    /* Mensaje informativo si falta uno de los valores */
    if (data.mensaje) {
      mostrarAlertaComp('aviso', data.mensaje);
    }

    if (seccion) seccion.classList.remove('oculto');

  } catch (err) {
    const esTimeout = err.name === 'TimeoutError' || err.name === 'AbortError';
    mostrarAlertaComp('error', esTimeout
      ? 'La comparación tardó demasiado. Intente nuevamente.'
      : 'No se pudo conectar con el servidor.');
    const seccion = document.getElementById('seccion-comparacion');
    if (seccion) seccion.classList.add('oculto');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Comparar'; }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('btn-comparar');
  if (btn) {
    btn.addEventListener('click', () => {
      const productoId = document.getElementById('sel-producto-comp')?.value;
      const periodo    = document.getElementById('sel-periodo-comp')?.value;
      consultarComparacion(productoId, periodo);
    });
  }
});

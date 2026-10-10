/**
 * historicos.js — RF01 y RF02
 * Conecta con el backend FastAPI en lugar de datos simulados.
 * GET  /historicos?producto_id=X  → RF01
 * POST /predicciones              → RF02
 */

const API_BASE = 'http://localhost:8000';

/* ── Utilidades ──────────────────────────────────────────── */
function mostrarAlerta(idAlerta, tipo, mensaje) {
  const el = document.getElementById(idAlerta);
  if (!el) return;
  el.className = `alerta alerta--${tipo}`;
  el.textContent = mensaje;
}

function ocultarAlerta(idAlerta) {
  const el = document.getElementById(idAlerta);
  if (el) el.className = 'alerta alerta--oculta';
}

/* ── Poblar selectores desde el backend ──────────────────── */
async function cargarProductos() {
  try {
    const resp = await fetch(`${API_BASE}/productos`, { signal: AbortSignal.timeout(5000) });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    const selects = document.querySelectorAll('.select-producto');
    selects.forEach(sel => {
      data.productos.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.id_producto;
        opt.textContent = `${p.nombre} (${p.categoria})`;
        sel.appendChild(opt);
      });
    });
  } catch {
    /* Si el backend no está disponible, usa los datos simulados como fallback */
    if (typeof PRODUCTOS !== 'undefined') {
      const selects = document.querySelectorAll('.select-producto');
      selects.forEach(sel => {
        PRODUCTOS.forEach(p => {
          const opt = document.createElement('option');
          opt.value = p.id;
          opt.textContent = `${p.nombre} (${p.categoria})`;
          sel.appendChild(opt);
        });
      });
    }
  }
}

function poblarSelectSemanas() {
  const sel = document.getElementById('sel-semana');
  if (!sel || typeof SEMANAS_DISPONIBLES === 'undefined') return;
  SEMANAS_DISPONIBLES.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.valor;
    opt.textContent = s.etiqueta;
    sel.appendChild(opt);
  });
}

/* ── RF01: Consultar históricos ──────────────────────────── */
async function consultarHistoricos() {
  const productoId = document.getElementById('sel-producto-hist').value;
  const btnConsultar = document.getElementById('btn-consultar-hist');
  const seccion = document.getElementById('seccion-historicos');
  const cuerpoTabla = document.getElementById('cuerpo-tabla-hist');

  if (!productoId) {
    mostrarAlerta('alerta-hist', 'aviso', 'Seleccione un producto antes de consultar.');
    return;
  }

  ocultarAlerta('alerta-hist');
  btnConsultar.disabled = true;
  btnConsultar.innerHTML = '<span class="spinner"></span> Consultando…';

  try {
    const resp = await fetch(
      `${API_BASE}/historicos?producto_id=${productoId}`,
      { signal: AbortSignal.timeout(5000) }
    );
    const data = await resp.json();

    if (resp.status === 404) {
      mostrarAlerta('alerta-hist', 'error', data.detalle || 'Producto no encontrado.');
      seccion.classList.add('oculto');
      return;
    }

    if (resp.status === 503) {
      mostrarAlerta('alerta-hist', 'error',
        (data.detalle || 'Servidor de datos no disponible.') +
        ' — ' + (data.reintento || 'Intente nuevamente.'));
      seccion.classList.add('oculto');
      return;
    }

    const historicos = data.historicos || [];

    if (!historicos.length) {
      mostrarAlerta('alerta-hist', 'aviso',
        data.mensaje || 'No existen registros históricos disponibles para el producto seleccionado.');
      seccion.classList.add('oculto');
      return;
    }

    /* RF01-CA2: ya vienen ordenados ASC por el backend */
    document.getElementById('titulo-tabla-hist').textContent =
      `Datos históricos — ${data.nombre_producto}`;

    cuerpoTabla.innerHTML = '';
    historicos.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${r.periodo}</td>
        <td>${r.nombre_producto}</td>
        <td class="texto-der negrita">${Number(r.demanda_real).toLocaleString('es-PE')}</td>
        <td class="texto-centro"><span class="badge badge--verde">unidad</span></td>`;
      cuerpoTabla.appendChild(tr);
    });

    document.getElementById('conteo-registros').textContent =
      `${historicos.length} registro${historicos.length !== 1 ? 's' : ''}`;

    seccion.classList.remove('oculto');

  } catch (err) {
    if (err.name === 'TimeoutError' || err.name === 'AbortError') {
      mostrarAlerta('alerta-hist', 'error',
        'El servidor de datos no respondió en 5 segundos. Intente nuevamente.');
    } else {
      mostrarAlerta('alerta-hist', 'error',
        'No se pudo conectar con el servidor. Verifique que el backend esté en ejecución.');
    }
    seccion.classList.add('oculto');
  } finally {
    btnConsultar.disabled = false;
    btnConsultar.textContent = 'Consultar históricos';
  }
}

/* ── RF02: Generar predicción ────────────────────────────── */
async function generarPrediccion() {
  const productoId = document.getElementById('sel-producto-pred').value;
  const semana     = document.getElementById('sel-semana').value;
  const btnGenerar = document.getElementById('btn-generar-pred');
  const seccion    = document.getElementById('seccion-prediccion');

  if (!productoId || !semana) {
    mostrarAlerta('alerta-pred', 'aviso', 'Seleccione un producto y un periodo antes de generar la predicción.');
    return;
  }

  ocultarAlerta('alerta-pred');
  btnGenerar.disabled = true;
  btnGenerar.innerHTML = '<span class="spinner"></span> Generando…';

  try {
    const resp = await fetch(`${API_BASE}/predicciones`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ producto_id: parseInt(productoId, 10), periodo: semana }),
      signal: AbortSignal.timeout(30000), // Gemini puede tardar más
    });
    const data = await resp.json();

    if (resp.status === 404) {
      mostrarAlerta('alerta-pred', 'error', data.detalle || 'Producto no encontrado.');
      seccion.classList.add('oculto');
      return;
    }

    if (resp.status === 422) {
      mostrarAlerta('alerta-pred', 'error', data.detalle || 'Datos históricos insuficientes.');
      seccion.classList.add('oculto');
      return;
    }

    if (resp.status === 503) {
      mostrarAlerta('alerta-pred', 'error', data.detalle || 'El servicio de predicción no está disponible.');
      seccion.classList.add('oculto');
      return;
    }

    /* RF02-CA4: mostrar nombre, periodo y cantidad */
    document.getElementById('pred-producto').textContent = data.nombre_producto;
    document.getElementById('pred-periodo').textContent  = data.periodo;
    document.getElementById('pred-valor').textContent    = Number(data.cantidad_estimada).toLocaleString('es-PE');
    document.getElementById('pred-unidad').textContent   = 'unidades';

    /* RF02-CA6: notificar si fue actualización */
    const alertaEl = document.getElementById('alerta-pred-actualizada');
    if (data.actualizado) {
      alertaEl.classList.remove('oculto');
    } else {
      alertaEl.classList.add('oculto');
    }

    seccion.classList.remove('oculto');

  } catch (err) {
    if (err.name === 'TimeoutError' || err.name === 'AbortError') {
      mostrarAlerta('alerta-pred', 'error',
        'El servicio de predicción tardó demasiado. Intente nuevamente.');
    } else {
      mostrarAlerta('alerta-pred', 'error',
        'No se pudo conectar con el servidor. Verifique que el backend esté en ejecución.');
    }
    seccion.classList.add('oculto');
  } finally {
    btnGenerar.disabled = false;
    btnGenerar.textContent = 'Generar predicción';
  }
}

/* ── Bootstrap ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  cargarProductos();
  poblarSelectSemanas();

  // También poblar el select de periodo de comparación con las mismas semanas
  const selPeriodoComp = document.getElementById('sel-periodo-comp');
  if (selPeriodoComp && typeof SEMANAS_DISPONIBLES !== 'undefined') {
    SEMANAS_DISPONIBLES.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.valor;
      opt.textContent = s.etiqueta;
      selPeriodoComp.appendChild(opt);
    });
  }

  document.getElementById('btn-consultar-hist')
    .addEventListener('click', consultarHistoricos);

  document.getElementById('btn-generar-pred')
    .addEventListener('click', generarPrediccion);

  document.getElementById('btn-limpiar-hist')
    .addEventListener('click', () => {
      document.getElementById('seccion-historicos').classList.add('oculto');
      document.getElementById('sel-producto-hist').selectedIndex = 0;
      ocultarAlerta('alerta-hist');
    });
});

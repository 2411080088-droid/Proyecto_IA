# Revisión cruzada — Sesión 7

> **Nota:** No hubo intercambio de repositorios entre equipos durante el laboratorio.
> Esta revisión se realiza sobre el módulo propio (H-RF01) como autorrevisión,
> declarando honestamente la situación a la docente.
> Revisor: Huaman Huari, Jefry Rodrigo · Equipo: 4
> Módulo revisado: H-RF01 — Consulta de datos históricos de demanda

---

## Lista de cotejo aplicada

Archivos revisados:
- `web/routes/web.php`
- `web/app/Http/Controllers/HistoricoController.php`
- `web/app/Models/DatoHistorico.php`
- `web/resources/views/historicos/mostrar.blade.php`

| # | Criterio | Resultado |
|---|---|---|
| 1 | ¿Corre? | ✅ La ruta `GET /historicos/{id}` coincide con el método `mostrar()` del controlador |
| 2 | ¿Traza? | ✅ Todos los archivos inician con `// Historia: H-RF01` o `{{-- Historia: H-RF01` |
| 3 | ¿Valida? | ✅ Restricción `->where('id', '[0-9]+')` en la ruta; `abort(404)` en el controlador |
| 4 | ¿Parametriza? | ✅ Todas las consultas usan Eloquent parametrizado; no hay `DB::raw` ni concatenación |
| 5 | ¿Protege? | ✅ No hay claves ni contraseñas en el código; `.env` está en `.gitignore` |
| 6 | ¿Respeta el diseño? | ⚠️ Ver Hallazgo 1 |

---

## HALLAZGO 1 · Deuda técnica

**Revisor:** Huaman Huari, Jefry Rodrigo · **Equipo revisado:** 4 (autorrevisión) · **Módulo:** H-RF01

**Archivo y línea:** `web/resources/views/historicos/mostrar.blade.php`, líneas 8–35

**Criterio incumplido:** 6 · Respeta el diseño

**Qué observé:** los estilos CSS están escritos directamente en la etiqueta `<style>` dentro de la vista, en lugar de usar un layout compartido (`@extends`) con una hoja de estilos separada. Cada vista repite la misma paleta de colores y tipografía de forma independiente.

**Por qué importa:** si se cambia el color corporativo o la fuente, hay que modificar cada vista por separado. En un sistema con 5 módulos (RF01–RF05) eso es cinco archivos a editar manualmente, con riesgo de inconsistencias visuales. Es deuda de mantenimiento.

**Corrección propuesta:**
1. Crear `web/resources/views/layouts/app.blade.php` con el HTML base, la cabecera y los estilos comunes.
2. En cada vista reemplazar el HTML completo por:
```blade
@extends('layouts.app')
@section('titulo', 'Históricos — ' . $producto->nombre)
@section('contenido')
    {{-- solo el contenido específico --}}
@endsection
```

**Severidad:** deuda técnica (no rompe funcionalidad, pero aumenta el costo de mantenimiento)

---

## HALLAZGO 2 · Deuda técnica

**Revisor:** Huaman Huari, Jefry Rodrigo · **Equipo revisado:** 4 (autorrevisión) · **Módulo:** H-RF01

**Archivo y línea:** `web/app/Http/Controllers/HistoricoController.php`, línea 18

**Criterio incumplido:** 6 · Respeta el diseño

**Qué observé:** el parámetro `$id` llega como `int` en la firma del método (`public function mostrar(int $id)`), pero la restricción de ruta `[0-9]+` no garantiza que el valor quepa en un entero PHP en todos los entornos. Si alguien envía un número muy grande como `99999999999999`, PHP puede truncarlo silenciosamente antes de que llegue a la consulta Eloquent.

**Por qué importa:** la consulta devolvería `null` (404 correcto), pero el comportamiento depende del tamaño del entero en el sistema operativo, no de una validación explícita. Es inconsistente entre plataformas de 32 y 64 bits.

**Corrección propuesta:** agregar validación explícita con un rango razonable:
```php
if ($id <= 0 || $id > 999999) {
    abort(404);
}
```
O usar `Route::get('/historicos/{id}', ...)->whereNumber('id')` con un middleware de validación de rango.

**Severidad:** deuda técnica (bajo riesgo en este contexto de datos simulados, pero relevante en producción)

---

## HALLAZGO 3 · Deuda técnica

**Revisor:** Huaman Huari, Jefry Rodrigo · **Equipo revisado:** 4 (autorrevisión) · **Módulo:** H-RF01

**Archivo y línea:** `web/app/Http/Controllers/HistoricoController.php`, línea 8

**Criterio incumplido:** 6 · Respeta el diseño

**Qué observé:** se importa `Illuminate\Http\Request` (`use Illuminate\Http\Request`) pero el método `mostrar()` no recibe ni usa un objeto `Request`. El import es innecesario.

**Por qué importa:** no causa errores, pero genera ruido en el código y puede confundir a quien lo lea pensando que hay validación de request que no existe.

**Corrección propuesta:** eliminar la línea `use Illuminate\Http\Request;` del controlador.

**Severidad:** deuda técnica mínima (cosmética)

---

## Conclusión

El módulo cumple los criterios de seguridad y funcionalidad (criterios 1–5). Los tres hallazgos son de deuda técnica, no de seguridad ni de errores funcionales. El más relevante para mantenimiento futuro es el Hallazgo 1 (ausencia de layout compartido), que deberá resolverse antes de agregar los módulos RF02–RF05 a la capa Laravel para evitar duplicación masiva de estilos.

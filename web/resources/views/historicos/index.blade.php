{{-- Historia: H-RF01 — Consulta de datos históricos de demanda --}}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Productos — Predicción de Demanda</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f5f7f8; color: #263238; margin: 0; }
        header { background: #1a6e3c; color: #fff; padding: 1rem 2rem; }
        header h1 { margin: 0; font-size: 1.2rem; }
        header p  { margin: .2rem 0 0; font-size: .8rem; opacity: .8; }
        main { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
        h2 { color: #1a6e3c; margin-bottom: 1rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
        .card { background: #fff; border: 1px solid #cfd8dc; border-radius: 8px; padding: 1rem;
                text-decoration: none; color: inherit; transition: box-shadow .2s; }
        .card:hover { box-shadow: 0 3px 10px rgba(0,0,0,.15); }
        .card__nombre { font-weight: 700; color: #1a6e3c; }
        .card__cat    { font-size: .8rem; color: #546e7a; margin-top: .3rem; }
        .vacio { color: #546e7a; font-style: italic; }
        footer { text-align: center; padding: 1rem; font-size: .75rem; color: #546e7a;
                 border-top: 1px solid #cfd8dc; margin-top: 2rem; }
    </style>
</head>
<body>

<header>
    <h1>Predicción de Demanda — Supermercados Peruanos S.A.</h1>
    <p>Consulta de datos históricos · RF01</p>
</header>

<main>
    <h2>Selecciona un producto</h2>

    @if ($productos->isEmpty())
        <p class="vacio">No hay productos activos registrados.</p>
    @else
        <div class="grid">
            @foreach ($productos as $p)
                <a href="{{ url('/historicos/' . $p->id_producto) }}" class="card">
                    <div class="card__nombre">{{ $p->nombre }}</div>
                    <div class="card__cat">{{ $p->unidad_medida }}</div>
                </a>
            @endforeach
        </div>
    @endif
</main>

<footer>Sistema de predicción de demanda · Datos simulados</footer>

</body>
</html>

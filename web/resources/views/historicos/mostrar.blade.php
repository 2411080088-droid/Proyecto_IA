{{-- Historia: H-RF01 — Consulta de datos históricos de demanda --}}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Históricos — {{ $producto->nombre }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f5f7f8; color: #263238; margin: 0; }
        header { background: #1a6e3c; color: #fff; padding: 1rem 2rem; display: flex;
                 align-items: center; justify-content: space-between; }
        header h1 { margin: 0; font-size: 1.2rem; }
        header a  { color: rgba(255,255,255,.85); font-size: .85rem; text-decoration: none; }
        header a:hover { color: #fff; }
        main { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
        .titulo-seccion { color: #1a6e3c; margin-bottom: .5rem; }
        .badge { display: inline-block; background: #e8f5ee; color: #1a6e3c;
                 border-radius: 12px; padding: .2rem .7rem; font-size: .8rem; font-weight: 600; }
        table { width: 100%; border-collapse: collapse; background: #fff;
                border-radius: 8px; overflow: hidden;
                border: 1px solid #cfd8dc; font-size: .9rem; }
        thead tr { background: #1a6e3c; color: #fff; }
        thead th { padding: .65rem 1rem; text-align: left; font-size: .8rem; letter-spacing: .03em; }
        tbody tr { border-bottom: 1px solid #cfd8dc; }
        tbody tr:last-child { border-bottom: none; }
        tbody tr:hover { background: #e8f5ee; }
        tbody td { padding: .6rem 1rem; }
        .texto-der { text-align: right; }
        .vacio { text-align: center; padding: 2rem; color: #546e7a; font-style: italic; }
        .alerta { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80;
                  border-radius: 6px; padding: .75rem 1rem; margin-bottom: 1rem; font-size: .875rem; }
        footer { text-align: center; padding: 1rem; font-size: .75rem; color: #546e7a;
                 border-top: 1px solid #cfd8dc; margin-top: 2rem; }
    </style>
</head>
<body>

<header>
    <h1>Históricos de demanda — {{ $producto->nombre }}</h1>
    <a href="{{ url('/historicos') }}">← Volver a productos</a>
</header>

<main>
    <h2 class="titulo-seccion">
        Datos históricos
        <span class="badge">RF01</span>
        <span style="font-weight:400;font-size:.85rem;color:#546e7a">
            · {{ $historicos->count() }} registro{{ $historicos->count() !== 1 ? 's' : '' }}
        </span>
    </h2>

    {{-- RF01-CA3: mensaje informativo si no hay históricos --}}
    @if ($historicos->isEmpty())
        <div class="alerta">
            No existen registros históricos disponibles para <strong>{{ $producto->nombre }}</strong>.
        </div>
    @else
        {{-- RF01-CA2: ordenados por periodo ASC, formato AAAA-WNN --}}
        <table>
            <thead>
                <tr>
                    <th>Periodo</th>
                    <th>Producto</th>
                    <th class="texto-der">Demanda real</th>
                    <th>Unidad</th>
                </tr>
            </thead>
            <tbody>
                @foreach ($historicos as $h)
                    <tr>
                        <td>{{ $h->periodo }}</td>
                        <td>{{ $producto->nombre }}</td>
                        <td class="texto-der"><strong>{{ number_format($h->demanda_real, 0, ',', '.') }}</strong></td>
                        <td>{{ $producto->unidad_medida }}</td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    @endif
</main>

<footer>Sistema de predicción de demanda · Datos simulados · Supermercados Peruanos S.A.</footer>

</body>
</html>

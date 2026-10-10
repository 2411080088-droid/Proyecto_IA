<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

namespace App\Http\Controllers;

use App\Models\Producto;
use Illuminate\Http\Request;

class HistoricoController extends Controller
{
    /**
     * Muestra los datos históricos de demanda de un producto.
     * RF01-CA1: recupera todos los registros del producto vía Eloquent.
     * RF01-CA2: ordenados por periodo de forma ascendente (AAAA-WNN).
     * RF01-CA7: si el producto no existe, abort(404).
     */
    public function mostrar(int $id)
    {
        // RF01-CA7: producto no encontrado → 404 (distinto al caso sin históricos)
        $producto = Producto::where('id_producto', $id)
            ->where('activo', 1)
            ->first();

        if (! $producto) {
            abort(404, 'El producto solicitado no fue encontrado.');
        }

        // RF01-CA1 y CA2: históricos ordenados ASC por periodo (AAAA-WNN ordinal)
        $historicos = $producto->historicos()
            ->orderBy('periodo', 'asc')
            ->get();

        return view('historicos.mostrar', [
            'producto'   => $producto,
            'historicos' => $historicos,
        ]);
    }

    /**
     * Lista todos los productos activos para que el usuario elija.
     */
    public function index()
    {
        $productos = Producto::where('activo', 1)
            ->orderBy('nombre', 'asc')
            ->get();

        return view('historicos.index', [
            'productos' => $productos,
        ]);
    }
}

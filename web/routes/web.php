<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\HistoricoController;

Route::get('/', function () {
    return redirect('/historicos');
});

// RF01: listar productos activos
Route::get('/historicos', [HistoricoController::class, 'index'])
    ->name('historicos.index');

// RF01: mostrar históricos de un producto por id (solo enteros positivos)
// RF01-CA7: si el producto no existe → abort(404)
Route::get('/historicos/{id}', [HistoricoController::class, 'mostrar'])
    ->where('id', '[0-9]+')
    ->name('historicos.mostrar');

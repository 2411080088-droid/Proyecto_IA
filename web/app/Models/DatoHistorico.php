<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DatoHistorico extends Model
{
    // Tabla existente en SQLite — no crear migraciones
    protected $table = 'dato_historico';

    // La tabla no tiene created_at / updated_at
    public $timestamps = false;

    protected $primaryKey = 'id_dato_historico';

    protected $fillable = [
        'id_producto',
        'periodo',
        'demanda_real',
    ];

    /**
     * Producto al que pertenece este registro histórico.
     */
    public function producto()
    {
        return $this->belongsTo(Producto::class, 'id_producto', 'id_producto');
    }
}

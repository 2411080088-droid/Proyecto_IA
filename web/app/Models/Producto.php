<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Producto extends Model
{
    // Tabla existente en SQLite — no crear migraciones
    protected $table = 'producto';

    // La tabla no tiene created_at / updated_at
    public $timestamps = false;

    protected $primaryKey = 'id_producto';

    protected $fillable = [
        'id_categoria',
        'nombre',
        'unidad_medida',
        'activo',
    ];

    /**
     * Históricos de demanda asociados al producto.
     */
    public function historicos()
    {
        return $this->hasMany(DatoHistorico::class, 'id_producto', 'id_producto');
    }

    /**
     * Categoría a la que pertenece el producto.
     */
    public function categoria()
    {
        return $this->belongsTo(CategoriaProducto::class, 'id_categoria', 'id_categoria');
    }
}

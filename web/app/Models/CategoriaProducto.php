<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CategoriaProducto extends Model
{
    // Tabla existente en SQLite — no crear migraciones
    protected $table = 'categoria_producto';

    // La tabla no tiene created_at / updated_at
    public $timestamps = false;

    protected $primaryKey = 'id_categoria';

    protected $fillable = [
        'nombre',
        'descripcion',
    ];

    public function productos()
    {
        return $this->hasMany(Producto::class, 'id_categoria', 'id_categoria');
    }
}

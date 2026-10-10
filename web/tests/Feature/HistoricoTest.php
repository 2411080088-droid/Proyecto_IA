<?php
// Historia: H-RF01 — Consulta de datos históricos de demanda

namespace Tests\Feature;

use Tests\TestCase;

class HistoricoTest extends TestCase
{
    /**
     * RF01-CA1 y CA2: el producto 1 (Mango) existe en la BD y tiene históricos.
     * Verifica que la respuesta es 200 y contiene el nombre del producto.
     * NO usa RefreshDatabase ni migraciones — apunta a la BD existente.
     */
    public function test_producto_existente_responde_200_con_datos(): void
    {
        $response = $this->get('/historicos/1');

        $response->assertStatus(200);
        $response->assertSee('Mango');
    }

    /**
     * RF01-CA5 / CA7: un id que no existe debe responder 404, nunca 500.
     */
    public function test_producto_inexistente_responde_404(): void
    {
        $response = $this->get('/historicos/9999');

        $response->assertStatus(404);
    }

    /**
     * RF01: la página índice de productos responde 200.
     */
    public function test_indice_productos_responde_200(): void
    {
        $response = $this->get('/historicos');

        $response->assertStatus(200);
    }
}

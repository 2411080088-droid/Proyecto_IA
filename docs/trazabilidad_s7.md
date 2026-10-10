# Trazabilidad de tareas — Sesión 7

| N.º tarea | Título corto | Historia (H-xx) | Decisión | Justificación | Verificación (URL y resultado esperado) |
|---|---|---|---|---|---|
| 1 | Estructura del proyecto y dependencias | — | ELIMINAR · ya realizada | Directorios `app/`, `mcp_server/`, `requirements.txt`, `.env.example` y `.gitignore` ya existían en disco desde la sesión anterior | `Get-ChildItem app/, requirements.txt` → presentes |
| 2 | Base de datos SQLite con datos simulados | RF01, RF02 | ELIMINAR · ya realizada | `database/schema.sql` en SQLite, `init_db.py` ejecutado, `prediccion_demanda.db` con 70 históricos | `Test-Path database/prediccion_demanda.db` → `True` |
| 3 | Módulo de Configuración (RNF02) | RNF02 | ELIMINAR · ya realizada | `app/config/settings.py` con validación de `GEMINI_API_KEY` al arranque | `Get-Content app/config/settings.py` → función `_require_env` presente |
| 4 | Servidor MCP solo lectura | RF06 | ELIMINAR · ya realizada | `mcp_server/main.py` con middleware HTTP 405 para métodos no-GET | `Get-Content mcp_server/main.py` → middleware `rechazar_escrituras` presente |
| 5 | Repositorio de Históricos | RF01 | ELIMINAR · ya realizada | `app/repositories/historicos_repo.py` con timeout 5 s y dataclass `DatoHistorico` | `Get-Content app/repositories/historicos_repo.py` → clase presente |
| 6 | Servicio y Router de Históricos | RF01 | ELIMINAR · ya realizada | `app/services/historicos_service.py` y `app/routers/historicos_router.py` registrados en `main.py` | `Get-Content app/routers/historicos_router.py` → endpoint `GET /historicos` |
| 7 | Cliente Gemini | RF02 | ELIMINAR · ya realizada | `app/integrations/gemini_client.py` con prompt, parseo y manejo de errores | `Get-Content app/integrations/gemini_client.py` → función `generar_pronostico` |
| 8 | Repositorio de Predicciones | RF02, RF03 | ELIMINAR · ya realizada | `app/repositories/predicciones_repo.py` con `insertar_o_actualizar`, `obtener_predicciones` y `obtener_prediccion` | Tres funciones presentes en el archivo |
| 9 | Servicio y Router de Predicciones | RF02, RF03 | ELIMINAR · ya realizada | `app/routers/predicciones_router.py` con `POST` y `GET /predicciones` | Dos endpoints presentes |
| 10 | Repositorio de Comparación y Router | RF04 | ELIMINAR · ya realizada | `app/routers/comparacion_router.py` con `GET /comparacion` | Endpoint presente |
| 11 | Repositorio de Métricas y Router | RF05 | ELIMINAR · ya realizada | `app/routers/metricas_router.py` con `GET /metricas` | Endpoint presente |
| 12 | Adaptar esquema al formato AAAA-WNN | RF01, RF03, RF04, RF05 | MANTENER · completada | Formato `AAAA-WNN` confirmado en BD; `ORDER BY periodo ASC` en todos los repositorios; decisión registrada en `design.md` sección 7 | `SELECT periodo FROM dato_historico LIMIT 3` → `2024-W01`, `2024-W02`, `2024-W03` |
| 13 | Rebanada vertical Laravel — Históricos | RF01 | MANTENER | Primera rebanada vertical completa: ruta GET, controlador Eloquent, modelos sobre tablas existentes, vistas Blade. Sin migraciones ni seeders. | `http://127.0.0.1:8000/historicos/1` → lista datos de Mango; `http://127.0.0.1:8000/historicos/9999` → 404 |
| 14 | Prueba automatizada Laravel | RF01 | MANTENER | Cubre 200 con dato real y 404 con id inexistente. Usa BD existente, sin `RefreshDatabase`. | `cd web && php artisan test --filter=HistoricoTest` → 3 pruebas en verde |
| 15 | Verificar propiedades de corrección | RF01–RF06 | MANTENER | 7 propiedades de `requirements.md` pendientes de verificación manual con el backend en ejecución | Backend en `http://localhost:8000`; verificar cada propiedad según `tasks.md` tarea 14 |

## Notas

- Las tareas 1–11 fueron eliminadas porque corresponden al backend Python/FastAPI ya construido en sesiones anteriores.
- Las tareas 13 y 14 son nuevas, incorporadas en la Sesión 7 para cumplir con la rebanada vertical en Laravel según la guía de laboratorio.
- Historia faltante detectada: no existe una historia H-xx explícita para la capa de presentación Laravel en `requirements.md`; se usa el identificador del requisito funcional correspondiente (RF01, RF02, etc.).

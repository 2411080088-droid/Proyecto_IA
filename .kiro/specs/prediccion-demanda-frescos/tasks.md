# Tareas de Implementación — Predicción de Demanda de Productos Frescos

## Tarea 1: Configurar la estructura del proyecto y las dependencias
<!-- ELIMINADA · ya realizada: directorios app/, mcp_server/, config/, routers/, services/, repositories/, integrations/ creados; requirements.txt, .env.example y .gitignore presentes en disco -->

## Tarea 2: Crear y poblar la base de datos SQLite con datos simulados
<!-- ELIMINADA · ya realizada: database/schema.sql en sintaxis SQLite, database/init_db.py y database/prediccion_demanda.db (5 categorías, 7 productos, 70 históricos) existen en disco -->

## Tarea 3: Implementar el Módulo de Configuración (RNF02)
<!-- ELIMINADA · ya realizada: app/config/settings.py creado con validación de GEMINI_API_KEY al arranque -->

## Tarea 4: Implementar el Servidor MCP en modo solo lectura (RF06)
<!-- ELIMINADA · ya realizada: mcp_server/main.py creado con middleware que rechaza métodos distintos a GET con HTTP 405 -->

## Tarea 5: Implementar el Repositorio de Históricos (RF01, RF06)
<!-- ELIMINADA · ya realizada: app/repositories/historicos_repo.py creado con timeout de 5 s y mapeo a DatoHistorico -->

## Tarea 6: Implementar el Servicio y Router de Históricos (RF01)
<!-- ELIMINADA · ya realizada: app/services/historicos_service.py y app/routers/historicos_router.py creados y registrados en main.py -->

## Tarea 7: Implementar el Cliente Gemini (RF02, RNF02)
<!-- ELIMINADA · ya realizada: app/integrations/gemini_client.py creado con prompt, parseo de entero y manejo de errores -->

## Tarea 8: Implementar el Repositorio de Predicciones (RF02, RF03)
<!-- ELIMINADA · ya realizada: app/repositories/predicciones_repo.py con insertar_o_actualizar, obtener_predicciones y obtener_prediccion -->

## Tarea 9: Implementar el Servicio y Router de Predicciones (RF02, RF03)
<!-- ELIMINADA · ya realizada: app/services/predicciones_service.py y app/routers/predicciones_router.py con POST y GET /predicciones -->

## Tarea 10: Implementar el Repositorio de Comparación y su Router (RF04)
<!-- ELIMINADA · ya realizada: app/repositories/comparacion_repo.py, app/services/comparacion_service.py y app/routers/comparacion_router.py creados -->

## Tarea 11: Implementar el Repositorio de Métricas y su Router (RF05)
<!-- ELIMINADA · ya realizada: app/repositories/metricas_repo.py, app/services/metricas_service.py y app/routers/metricas_router.py creados -->

## Tarea 12: Adaptar el esquema al formato de periodo AAAA-WNN

- [x] 12.1 Confirmar con el equipo que el campo periodo se almacena como texto `AAAA-WNN` en SQLite y registrar la decisión en design.md sección 7
- [x] 12.2 Verificar que `database/init_db.py` genera todos los históricos con formato `AAAA-WNN` y no con fechas ISO
- [x] 12.3 Verificar que las consultas de comparación y métricas ordenan y filtran correctamente usando `AAAA-WNN` como valor ordinal comparable

## Tarea 13: Implementar el Frontend Web (RF01, RF02, RF03, RF04, RF05)

- [ ] 13.1 Verificar que `frontend/index.html` carga correctamente los selectores de producto y periodo para los módulos RF01, RF02 y RF04 conectados al backend real
- [ ] 13.2 Verificar que `frontend/js/historicos.js` llama a `GET /historicos` del backend y muestra la lista ordenada por periodo con mensajes de error y reintento
- [ ] 13.3 Verificar que `frontend/js/historicos.js` llama a `POST /predicciones` y muestra producto, periodo y cantidad estimada, con notificación de actualización (RF02-CA6)
- [ ] 13.4 Verificar que `frontend/resultados.html` y `frontend/js/resultados.js` llaman a `GET /predicciones` y muestran la lista ordenada por periodo AAAA-WNN con mensaje de reintento si supera 5 s
- [ ] 13.5 Verificar que `frontend/js/comparacion.js` llama a `GET /comparacion` y gestiona los casos de valor faltante y error 404/503
- [ ] 13.6 Verificar que `frontend/js/resultados.js` llama a `GET /metricas`, muestra MAE y MAPE con 4 decimales, unidades y el contador de pares excluidos del MAPE
- [ ] 13.7 Revisar `frontend/css/estilos.css` para confirmar que los nuevos elementos (sección comparación, KPIs de métricas) tienen estilos coherentes con el resto de la interfaz

## Tarea 14: Verificar las propiedades de corrección definidas en requirements.md

- [ ] 14.1 Verificar la Propiedad 1 (no negatividad): generar predicciones para distintos productos y periodos y confirmar que `cantidad_estimada >= 0` en todos los casos
- [ ] 14.2 Verificar la Propiedad 2 (completitud de campos): comprobar que toda respuesta exitosa contiene `nombre_producto`, `periodo` y `cantidad_estimada` sin valores nulos ni vacíos
- [ ] 14.3 Verificar la Propiedad 3 (orden ascendente de históricos): consultar históricos para un producto con varios registros y confirmar que están ordenados por periodo de forma ascendente
- [ ] 14.4 Verificar la Propiedad 4 (corrección de la diferencia): calcular manualmente `abs(prediccion - dato_real)` para varios pares y comparar con el valor retornado por `GET /comparacion`
- [ ] 14.5 Verificar la Propiedad 5 (idempotencia del MCP): llamar a `GET /historicos` dos veces para el mismo producto y confirmar que los resultados son idénticos y la base de datos no se modifica
- [ ] 14.6 Verificar la Propiedad 6 (error por datos insuficientes): usar un producto con menos de 4 registros históricos e intentar generar una predicción; confirmar que el sistema retorna HTTP 422 con mensaje de datos insuficientes
- [ ] 14.7 Verificar la Propiedad 7 (corrección del MAE): calcular manualmente el MAE para los pares comparables disponibles y compararlo con el valor del endpoint `GET /metricas`; la diferencia debe ser menor a 0,01

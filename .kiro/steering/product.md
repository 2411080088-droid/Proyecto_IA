# Producto · Predicción de la demanda de productos frescos y ultrafrescos

Redacta todos los documentos en español.

## Propósito

Desarrollar un prototipo que permita mejorar la estimación de la demanda de productos frescos y ultrafrescos en Supermercados Peruanos S.A., utilizando datos históricos simulados para generar predicciones.

El producto busca apoyar a los planificadores y al personal de abastecimiento mediante pronósticos de demanda, consultas de datos históricos y evaluación de la precisión de las predicciones.

## Usuarios

- Planificador de demanda: consulta datos históricos, genera y revisa predicciones de demanda y compara los resultados pronosticados con la demanda real.
- Personal de planificación y abastecimiento: consulta los resultados de las predicciones para apoyar la planificación del abastecimiento.
- Gerente de planificación y suministro: consulta indicadores generales y métricas de precisión del modelo.

## Lo que hace

- Predecir la demanda de productos frescos y ultrafrescos.
- Consultar datos históricos de demanda.
- Consultar pronósticos de demanda.
- Comparar la demanda pronosticada con la demanda real.
- Visualizar los resultados de las predicciones.
- Calcular y mostrar métricas de evaluación del modelo.
- Consultar información mediante el servidor MCP existente en modo de solo lectura.

## Lo que NO hace

- No realiza reposición automática de productos.
- No gestiona compras ni pedidos a proveedores.
- No administra la logística de los centros de distribución.
- No modifica el inventario real de Supermercados Peruanos S.A.
- No se integra directamente con los sistemas internos reales de Supermercados Peruanos S.A.
- No utiliza datos personales reales de clientes.
- No permite modificar ni eliminar datos mediante el servidor MCP.

## Reglas no negociables

- Se utilizarán datos simulados para el desarrollo y las pruebas.
- El servidor MCP desarrollado previamente deberá reutilizarse exclusivamente en modo de solo lectura.
- No se utilizarán datos personales reales.
- Si se llegaran a utilizar datos personales, deberá cumplirse la Ley N.° 29733 de Protección de Datos Personales.
- La solución deberá respetar estrictamente las funcionalidades declaradas dentro del alcance.
- No deberán agregarse funcionalidades declaradas fuera del alcance.
- Las predicciones deberán generarse únicamente cuando existan datos suficientes para realizar el análisis.
- Los resultados deberán mostrar información verificable, como producto, periodo, demanda estimada y métricas de evaluación.
# Requirements Document

## Introduction

Este documento describe los requisitos del prototipo de predicción de demanda de productos frescos y ultrafrescos para Supermercados Peruanos S.A. El sistema permite a los planificadores de demanda, al personal de abastecimiento y a los gerentes de planificación consultar datos históricos, generar pronósticos de demanda, comparar resultados con la demanda real y evaluar la precisión del modelo mediante métricas cuantitativas.

El sistema utiliza datos históricos simulados almacenados en SQLite, los expone mediante un servidor MCP propio en modo exclusivo de solo lectura, y emplea la API de Gemini para el análisis y la generación de pronósticos. El frontend es una interfaz web sencilla desarrollada en HTML y JavaScript, y el backend está construido con FastAPI sobre Python 3.11+.

El proyecto se desarrolla en un plazo de 10 semanas por un equipo de 4 integrantes. No se integra con sistemas internos reales de Supermercados Peruanos S.A. ni se utilizan datos personales reales.

---

## Glossary

- **Sistema**: El prototipo de predicción de demanda de productos frescos y ultrafrescos desarrollado para Supermercados Peruanos S.A.
- **Planificador**: Usuario con el rol de planificador de demanda que consulta datos históricos, genera predicciones y compara resultados.
- **Personal_Abastecimiento**: Usuario con el rol de personal de planificación y abastecimiento que consulta resultados de predicciones para apoyar la planificación.
- **Gerente**: Usuario con el rol de gerente de planificación y suministro que consulta indicadores generales y métricas de precisión.
- **Producto_Fresco**: Ítem de la categoría de productos frescos o ultrafrescos disponible en el catálogo simulado del Sistema.
- **Dato_Historico**: Registro de demanda o venta real de un Producto_Fresco para un periodo determinado, almacenado en la base de datos simulada.
- **Prediccion**: Valor numérico estimado de la demanda futura de un Producto_Fresco para un periodo determinado, generado por el Sistema.
- **Periodo**: Intervalo temporal (día, semana o mes) identificado por fecha de inicio y fecha de fin para el cual se consultan o generan datos.
- **Metrica_Evaluacion**: Indicador cuantitativo que expresa la precisión de las Predicciones respecto a los valores reales, como MAE (Error Absoluto Medio) o MAPE (Error Porcentual Absoluto Medio).
- **Servidor_MCP**: Servidor Message Control Protocol desarrollado en la semana 4 del proyecto, habilitado exclusivamente en modo de solo lectura, a través del cual el Sistema accede a los Datos_Historicos y a las Predicciones almacenadas.
- **API_Gemini**: Interfaz de programación de Google Gemini utilizada para el análisis de datos y la generación de pronósticos de demanda; su clave de acceso se almacena en una variable de entorno.
- **Base_Datos_Simulada**: Base de datos SQLite que contiene únicamente datos simulados sin información personal real, utilizada durante el desarrollo y las pruebas del proyecto.
- **Frontend**: Interfaz web del Sistema desarrollada en HTML y JavaScript que permite a los usuarios interactuar con las funcionalidades disponibles.
- **Backend**: Servicio web desarrollado en FastAPI (Python 3.11+) que procesa las solicitudes del Frontend y coordina la consulta de datos, la generación de predicciones y el cálculo de métricas.

---

## Requirements

### Requisito 1 (RF02): Generación de predicciones de demanda

**Historia de usuario:** Como Planificador, quiero generar una predicción de demanda de un Producto_Fresco para un Periodo determinado, para conocer la cantidad estimada que podría requerirse y apoyar la toma de decisiones de abastecimiento.

#### Criterios de aceptación

1. WHEN el Planificador selecciona un Producto_Fresco y un Periodo, THE Sistema SHALL verificar si existen al menos 4 registros de Datos_Historicos de periodos distintos del producto seleccionado antes de generar una Prediccion.
2. WHILE el Sistema ha verificado que existen datos históricos suficientes para un Producto_Fresco, WHEN el Planificador confirma el Periodo solicitado, THE Sistema SHALL generar una Prediccion con un valor numérico entero no negativo expresado en unidades del Producto_Fresco.
3. IF el Planificador selecciona un Producto_Fresco y un Periodo y el Sistema determina que no existen datos históricos suficientes para realizar el análisis, THEN THE Sistema SHALL mostrar un mensaje de error indicando que no es posible generar una predicción por falta de datos históricos.
4. WHEN el Sistema genera una Prediccion, THE Sistema SHALL mostrar al menos el nombre del Producto_Fresco, el Periodo solicitado y el valor numérico de la demanda estimada.
5. IF el Backend no puede establecer comunicación con la API_Gemini durante la generación de una Prediccion, THEN THE Sistema SHALL mostrar un mensaje de error indicando que el servicio de predicción no está disponible.
6. IF ya existe una Prediccion para el mismo Producto_Fresco y Periodo en la Base_Datos_Simulada, THEN THE Sistema SHALL sobrescribir el valor anterior con la nueva Prediccion generada y notificar al Planificador que el registro fue actualizado.

---

### Requisito 2 (RF01): Consulta de datos históricos de demanda

**Historia de usuario:** Como Planificador, quiero consultar los Datos_Historicos de demanda de un Producto_Fresco, para conocer la información empleada por el modelo en la generación de predicciones.

#### Criterios de aceptación

1. WHEN el Planificador consulta un Producto_Fresco, THE Sistema SHALL recuperar todos los registros de Datos_Historicos disponibles para dicho producto a través del Servidor_MCP.
2. WHEN el Sistema recupera los registros de Datos_Historicos de un Producto_Fresco, THE Sistema SHALL mostrarlos ordenados por fecha de forma ascendente en formato AAAA-MM-DD, indicando para cada registro la fecha, el nombre del Producto_Fresco y el valor de demanda registrado como número entero no negativo.
3. IF el Planificador consulta un Producto_Fresco para el cual no existen registros de Datos_Historicos en la Base_Datos_Simulada, THEN THE Sistema SHALL mostrar un mensaje informativo indicando que no existen registros históricos disponibles para el producto seleccionado.
4. THE Servidor_MCP SHALL exponer únicamente operaciones de lectura, sin aceptar solicitudes de escritura, modificación o eliminación de registros de Datos_Historicos.
5. WHEN el Sistema recupera los registros de Datos_Historicos de un Producto_Fresco en una Base_Datos_Simulada SQLite sin carga concurrente, THE Sistema SHALL completar la operación en un tiempo máximo de 5 segundos medido desde el envío de la consulta hasta la visualización de los resultados.
6. IF el Servidor_MCP no responde en un plazo de 5 segundos desde el envío de la consulta por parte del Sistema, THEN THE Sistema SHALL mostrar un mensaje de error indicando que el servidor de datos no está disponible e incluir una opción de reintento.
7. IF el Planificador consulta un identificador de Producto_Fresco que no existe en la Base_Datos_Simulada, THEN THE Sistema SHALL mostrar un mensaje de error indicando que el producto no fue encontrado, distinto del mensaje de ausencia de historial del criterio 3.

---

### Requisito 3 (RF04): Comparación de demanda pronosticada con demanda real

**Historia de usuario:** Como Planificador, quiero comparar la demanda pronosticada con la demanda real registrada para un mismo Producto_Fresco y Periodo, para evaluar visualmente la precisión del modelo.

#### Criterios de aceptación

1. WHEN el Planificador solicita la comparación para un Producto_Fresco y un Periodo, THE Sistema SHALL verificar si existe tanto una Prediccion como un Dato_Historico registrado para el mismo Producto_Fresco y Periodo.
2. IF el Sistema verifica que existen una Prediccion y un Dato_Historico para el mismo Producto_Fresco y Periodo, THEN THE Sistema SHALL mostrar el nombre del Producto_Fresco, el Periodo, el valor de la Prediccion, el valor del Dato_Historico y la diferencia absoluta |Prediccion − Dato_Historico| expresada en las mismas unidades que ambos valores.
3. IF el Planificador solicita la comparación para un Producto_Fresco que no existe en la Base_Datos_Simulada, THEN THE Sistema SHALL mostrar un mensaje de error indicando que el producto no fue encontrado. IF el Planificador solicita la comparación para un Producto_Fresco y un Periodo para los cuales no existe la Prediccion o el Dato_Historico, THEN THE Sistema SHALL mostrar el valor disponible y un mensaje informativo indicando cuál de los dos valores no está disponible.
4. WHEN el Sistema muestra la comparación en una Base_Datos_Simulada SQLite con un único usuario concurrente, THE Sistema SHALL completar la operación en un tiempo máximo de 5 segundos.

---

### Requisito 4 (RF03): Visualización de resultados de predicciones

**Historia de usuario:** Como Personal_Abastecimiento, quiero visualizar los resultados de las predicciones generadas por el modelo, para disponer de información que apoye la planificación del abastecimiento.

#### Criterios de aceptación

1. WHEN el Personal_Abastecimiento accede al módulo de resultados, THE Sistema SHALL mostrar la lista de Predicciones generadas indicando para cada registro el nombre del Producto_Fresco, el Periodo en formato AAAA-WNN (año-semana) y la cantidad estimada expresada en unidades enteras.
2. WHEN el Sistema muestra la lista de Predicciones, THE Sistema SHALL ordenarlas por Periodo de forma ascendente tratando el formato AAAA-WNN como valor ordinal comparable, como comportamiento por defecto.
3. IF no existen Predicciones generadas en la Base_Datos_Simulada al momento de acceder al módulo de resultados, THEN THE Sistema SHALL mostrar un mensaje informativo indicando que aún no se han generado predicciones.
4. WHEN el Personal_Abastecimiento accede al módulo de resultados con hasta 500 registros en la Base_Datos_Simulada, THE Sistema SHALL completar la carga y presentación de datos en un tiempo máximo de 5 segundos.
5. IF la carga del módulo de resultados supera los 5 segundos, THEN THE Sistema SHALL mostrar un mensaje de error indicando que la operación tardó demasiado e incluir una opción de reintento.

---

### Requisito 5 (RF05): Cálculo y visualización de métricas de evaluación del modelo

**Historia de usuario:** Como Gerente, quiero consultar un indicador de precisión del modelo, para conocer qué tan cercanas son las predicciones a los valores reales y tomar decisiones informadas sobre la planificación del abastecimiento.

#### Criterios de aceptación

1. WHEN el Gerente consulta la evaluación del modelo, THE Sistema SHALL calcular y mostrar el MAE (Error Absoluto Medio) y el MAPE (Error Porcentual Absoluto Medio), cada uno expresado como número decimal con exactamente 4 decimales.
2. WHEN el Sistema calcula una Metrica_Evaluacion, THE Sistema SHALL utilizar únicamente los pares de valores para los que exista tanto una Prediccion como un Dato_Historico para el mismo Producto_Fresco y Periodo.
3. IF el Gerente consulta la evaluación del modelo y el Sistema determina que no existen pares de Prediccion y Dato_Historico comparables disponibles, THEN THE Sistema SHALL mostrar un mensaje informativo indicando que no es posible calcular métricas por falta de datos comparables.
4. WHEN el Sistema muestra las métricas de evaluación, THE Sistema SHALL identificar el nombre de cada métrica (MAE y MAPE), su valor numérico con exactamente 4 decimales, y la unidad o escala correspondiente: el MAE en las mismas unidades de demanda del Producto_Fresco y el MAPE en porcentaje (%).
5. WHEN el Gerente consulta la evaluación del modelo, THE Sistema SHALL completar el cálculo y presentación de métricas en un tiempo máximo de 5 segundos bajo las condiciones del entorno de prueba del proyecto.
6. IF al calcular el MAPE el Sistema encuentra un par (Prediccion, Dato_Historico) donde el Dato_Historico es igual a cero, THEN THE Sistema SHALL excluir ese par del cálculo del MAPE y notificar al Gerente la cantidad de pares excluidos por este motivo.

---

### Requisito 6 (RF06): Acceso exclusivo de lectura mediante el Servidor MCP

**Historia de usuario:** Como Planificador, quiero que el Sistema consulte los datos almacenados exclusivamente mediante el Servidor_MCP en modo de solo lectura, para garantizar la integridad de la Base_Datos_Simulada durante el uso del prototipo.

#### Criterios de aceptación

1. THE Servidor_MCP SHALL aceptar únicamente operaciones HTTP GET o equivalentes de solo lectura definidas en su contrato de interfaz, rechazando cualquier solicitud de escritura, inserción, modificación o eliminación enviada desde el Sistema.
2. WHEN el Sistema realiza una consulta a través del Servidor_MCP, THE Servidor_MCP SHALL retornar los datos solicitados sin alterar ningún registro de la Base_Datos_Simulada; IF la consulta no produce resultados, THEN THE Servidor_MCP SHALL retornar una lista vacía.
3. IF el Sistema envía al Servidor_MCP una solicitud que implique modificación o eliminación de datos, THEN THE Servidor_MCP SHALL rechazar la solicitud con un código de error HTTP 405 (Método no permitido).
4. IF el Servidor_MCP rechaza una solicitud por ser de escritura, modificación o eliminación, THEN THE Servidor_MCP SHALL retornar un mensaje de error indicando que la operación no está permitida.
5. THE Base_Datos_Simulada SHALL contener únicamente datos simulados sin información personal real, en cumplimiento con las restricciones del proyecto y de la Ley N.° 29733 de Protección de Datos Personales.

---

### Requisito 7 (RNF02): Gestión segura de la clave de la API de Gemini

**Historia de usuario:** Como desarrollador del equipo, quiero que la clave de acceso a la API_Gemini se almacene exclusivamente en una variable de entorno, para evitar que quede expuesta en el código fuente o en los repositorios del proyecto.

#### Criterios de aceptación

1. THE Backend SHALL leer la clave de acceso a la API_Gemini exclusivamente desde una variable de entorno definida en el entorno de ejecución; IF la variable está definida pero su valor es vacío o en blanco, THEN THE Backend SHALL tratarla como no definida.
2. IF la variable de entorno que contiene la clave de la API_Gemini no está definida o su valor es vacío al momento del arranque, THEN THE Backend SHALL rechazar el inicio del servicio y mostrar un mensaje de error indicando que la variable de entorno requerida no está configurada.
3. THE Sistema SHALL no incluir la clave de la API_Gemini de forma literal en ningún archivo de código fuente, archivo de configuración ni en el historial del repositorio Git del proyecto; los archivos que puedan contener secretos (como .env) SHALL estar incluidos en el .gitignore del repositorio.

---

## Propiedades de Corrección (Property-Based Testing)

Las siguientes propiedades deben verificarse mediante pruebas basadas en propiedades (Property-Based Testing) para garantizar la corrección del Sistema más allá de casos de ejemplo individuales.

### Propiedad 1: Invariante de no negatividad de predicciones

**Requisito relacionado:** RF02 — Criterio 2

**Descripción:** Para cualquier Producto_Fresco y Periodo con datos históricos suficientes, la cantidad estimada devuelta por el Sistema siempre debe ser un número entero no negativo.

**Patrón:** Invariante

```
PARA TODO (producto, periodo) tales que existen datos históricos suficientes:
    prediccion = Sistema.generar_prediccion(producto, periodo)
    ENTONCES prediccion.cantidad_estimada >= 0
```

**Justificación:** Una demanda estimada negativa es un valor inválido para cualquier Producto_Fresco. Esta propiedad verifica que el modelo no produce resultados fuera del dominio válido independientemente del producto o periodo ingresado.

---

### Propiedad 2: Invariante de completitud de campos en la respuesta de predicción

**Requisito relacionado:** RF02 — Criterio 4; RF03 — Criterio 1

**Descripción:** Toda respuesta de predicción exitosa debe incluir siempre los tres campos obligatorios: nombre del Producto_Fresco, Periodo y cantidad estimada; ninguno de ellos puede ser nulo ni vacío.

**Patrón:** Invariante

```
PARA TODO (producto, periodo) tales que la predicción es exitosa:
    respuesta = Sistema.generar_prediccion(producto, periodo)
    ENTONCES respuesta.producto != nulo Y respuesta.periodo != nulo Y respuesta.cantidad_estimada != nulo
```

**Justificación:** Verifica que el contrato de la respuesta del Backend se cumple para cualquier entrada válida, garantizando que el Frontend siempre recibe los campos necesarios para la visualización.

---

### Propiedad 3: Consistencia del ordenamiento de datos históricos

**Requisito relacionado:** RF01 — Criterio 2

**Descripción:** Para cualquier Producto_Fresco con más de un registro histórico, los Datos_Historicos devueltos siempre deben estar ordenados por fecha de forma estrictamente ascendente.

**Patrón:** Invariante

```
PARA TODO producto tal que len(datos_historicos(producto)) > 1:
    registros = Sistema.consultar_historicos(producto)
    PARA TODO i en 0..len(registros)-2:
        ENTONCES registros[i].fecha <= registros[i+1].fecha
```

**Justificación:** El orden cronológico es un requisito explícito del RF01. Esta propiedad garantiza que el invariante se mantiene para cualquier conjunto de registros, no solo para los casos de prueba manuales.

---

### Propiedad 4: Corrección del cálculo de diferencia en la comparación

**Requisito relacionado:** RF04 — Criterio 2

**Descripción:** Para cualquier par (Prediccion, Dato_Historico) del mismo Producto_Fresco y Periodo, la diferencia mostrada por el Sistema debe ser igual al valor absoluto de la resta entre la predicción y el valor real.

**Patrón:** Metamórfica

```
PARA TODO (prediccion, dato_real) del mismo (producto, periodo):
    resultado = Sistema.comparar(producto, periodo)
    ENTONCES resultado.diferencia == abs(prediccion.cantidad_estimada - dato_real.valor)
```

**Justificación:** Verifica que el cálculo de diferencia es aritméticamente correcto para cualquier par de valores, incluyendo casos donde la predicción supera o es menor al valor real.

---

### Propiedad 5: Idempotencia de la consulta de datos históricos

**Requisito relacionado:** RF01 — Criterio 1; RF06 — Criterio 2

**Descripción:** Consultar los Datos_Historicos de un Producto_Fresco múltiples veces a través del Servidor_MCP debe producir siempre el mismo resultado sin modificar la Base_Datos_Simulada.

**Patrón:** Idempotencia

```
PARA TODO producto:
    resultado1 = Servidor_MCP.consultar_historicos(producto)
    resultado2 = Servidor_MCP.consultar_historicos(producto)
    ENTONCES resultado1 == resultado2
```

**Justificación:** Verifica que el Servidor_MCP opera en modo exclusivo de solo lectura y no produce efectos secundarios sobre los datos almacenados. Cualquier diferencia entre ejecuciones sucesivas indicaría una violación del requisito RF06.

---

### Propiedad 6: Condición de error para datos insuficientes

**Requisito relacionado:** RF02 — Criterio 3

**Descripción:** Para cualquier Producto_Fresco con menos de 4 registros de Datos_Historicos, el Sistema nunca debe generar una Prediccion; siempre debe retornar un error de datos insuficientes.

**Patrón:** Condición de error

```
PARA TODO producto tal que len(datos_historicos(producto)) < 4:
    resultado = Sistema.generar_prediccion(producto, cualquier_periodo)
    ENTONCES resultado.es_error == verdadero
    Y resultado.mensaje contiene indicación de datos insuficientes
```

**Justificación:** Garantiza que el umbral mínimo de datos para la generación de predicciones se respeta de forma consistente, evitando predicciones basadas en muestras estadísticamente no representativas.

---

### Propiedad 7: Corrección del cálculo de MAE

**Requisito relacionado:** RF05 — Criterios 1, 2 y 4

**Descripción:** El MAE (Error Absoluto Medio) calculado por el Sistema debe ser igual al promedio aritmético de las diferencias absolutas entre cada Prediccion y su Dato_Historico correspondiente.

**Patrón:** Modelo basado (implementación optimizada vs. implementación de referencia simple)

```
PARA TODO conjunto de pares comparables (predicciones, datos_reales) con len >= 1:
    mae_sistema = Sistema.calcular_metrica(predicciones, datos_reales, tipo="MAE")
    mae_referencia = sum(abs(p - r) para p, r en zip(predicciones, datos_reales)) / len(predicciones)
    ENTONCES abs(mae_sistema - mae_referencia) < 0.01
```

**Justificación:** Verifica mediante un modelo de referencia simple que el cálculo del MAE del Backend es aritméticamente equivalente a la definición formal, para cualquier conjunto de pares de valores.

# Stack y reglas técnicas

- Lenguaje: Python 3.11+.
- Framework: FastAPI, versión estable vigente [VERIFICAR].
- Base de datos: SQLite con datos simulados.
- Frontend: HTML y JavaScript simple.
- API externa: Gemini API.
- Secretos únicamente en variables de entorno; la clave de Gemini nunca debe escribirse directamente en el código ni versionarse en Git.
- Servidor MCP: únicamente en modo de solo lectura.
- Control de versiones: Git y GitHub.
- Nombres del proyecto y documentación: español.
- Todo módulo nuevo debe trazar a una historia o requisito existente en requirements.md; si no traza, no se construye.
- Las consultas y operaciones indicadas en requirements.md deben cumplir el límite máximo de 5 segundos bajo las condiciones de prueba definidas.
- No se utilizarán datos personales reales.
- No se realizará integración con los sistemas reales de Supermercados Peruanos S.A.
- El agente conversacional se difiere para una unidad posterior; esta semana únicamente se documentará el punto de extensión.
- No sustituir FastAPI, SQLite ni el frontend definido sin una enmienda previa del ADR-001.
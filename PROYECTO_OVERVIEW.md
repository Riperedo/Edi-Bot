# Resumen Ejecutivo: Edi-Bot
### Evolutionary & Differential Inference-Based Optimization Tool

Este documento detalla la visión, arquitectura, historial de desarrollo y la hoja de ruta del sistema de optimización híbrido diseñado para la resolución de parámetros en sistemas coloidales.

## 1. Descripción del Proyecto
El objetivo principal es proporcionar una herramienta robusta y eficiente para el ajuste de **Factores de Estructura Estáticos $S(q)$**. Mediante la combinación de un motor numérico de alto rendimiento en **C** y algoritmos de optimización global en **Python**, el sistema permite inferir parámetros físicos (como la fracción de volumen $\phi$, el diámetro de partícula $\sigma$, y parámetros de interacción de Yukawa) a partir de datos experimentales o de simulación.

### Arquitectura Técnica
- **Motor Numérico (C):** Basado en soluciones analíticas (Percus-Yevick para Esferas Duras y VMS-MSA para Doble Yukawa). Garantiza miles de evaluaciones por segundo.
- **Orquestador (Python):** Utiliza `scipy.optimize.differential_evolution` para explorar el espacio de parámetros de forma global, evitando mínimos locales espurios.
- **Capa de Reportes (LaTeX/PDF):** Un sistema automatizado que genera bitácoras técnicas detalladas, incluyendo gráficas de ajuste y tutoriales de replicación.

---

## 2. Historial de Desarrollo

### Fase 1: Cimientos y Conectividad
- **Integración del Motor en C:** Se portaron las funciones de factor de estructura desde la librería `structures`.
- **Wrapper Python-C:** Implementación de un puente mediante `subprocess` y archivos temporales para una comunicación eficiente.
- **Configuración Standalone:** Creación de la estructura `sq_optimizer` como una herramienta de consola independiente con su propio `README.md`.

### Fase 2: Precisión y Física Realista
- **Evolución Diferencial (DE):** Implementación del optimizador con extracción del "Top 3" de la población para ofrecer alternativas de ajuste al investigador.
- **Weighted MSE (Error Ponderado):** Ajuste de la función de costo para priorizar la región de bajos vectores de onda ($q$ pequeños), crucial para describir la estructura de largo alcance.
- **Generalización de $\sigma$:** Inclusión del parámetro de escala en todos los modelos para corregir desplazamientos en el eje $q$ derivados de la calibración experimental.

### Fase 3: Experiencia de Usuario y Reporting
- **Reporte Tutorial Acumulativo:** Transformación del reporte LaTeX en una bitácora que anexa resultados sin borrar los anteriores, incluyendo comandos de réplica.
- **Manual de Exploración:** Creación de `EXPLORACION_MANUAL.md` para permitir ajustes finos por parte del usuario.
- **Mejoras Estéticas:** Ajuste de leyendas y visualización de gráficas para una presentación profesional.

---

## 3. Estado Actual y Capacidades
El sistema es capaz de ajustar:
- **Modelo de Esferas Duras (HS):** Paratrización de $\phi$ y $\sigma$.
- **Modelos de Yukawa (Atractivo y Doble):** Paratrización de temperaturas efectidas, rangos de interacción y escala.
- **Optimización Batch:** Procesamiento automático de múltiples archivos `.dat` en una sola ejecución.

---

## 4. Próximos Pasos (Hoja de Ruta)

### Corto Plazo
1.  **Particle Swarm Optimization (PSO):** Implementar la búsqueda basada en enjambre de partículas para comparar la eficiencia de convergencia frente a DE.
2.  **Soporte Multi-Modelo Extendido:** Integración de la aproximación WCA (Weeks-Chandler-Andersen) y modelos para mezclas binarias.

### Mediano Plazo
1.  **Paralelización:** Implementar ejecución en paralelo para las evaluaciones de la población en DE/PSO, reduciendo significativamente los tiempos de ajuste en modelos complejos.
2.  **Interfaz Gráfica (GUI):** Desarrollo de un dashboard ligero (ej. Streamlit) para la visualización interactiva de los ajustes en tiempo real.
3.  **Detección Automática de Modelos:** Implementar heurísticas que sugieran qué modelo (HS, Yukawa, etc.) se ajusta mejor a la forma general de los datos antes de iniciar la optimización pesada.

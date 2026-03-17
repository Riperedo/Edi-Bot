# SQ Optimizer

Herramienta independiente basada en Python y C para el ajuste de curvas del factor de estructura estático $S(q)$ usando metaheurísticas de optimización global, inicialmente enfocada en el algoritmo de **Evolución Diferencial (Differential Evolution)**.

## Arquitectura Híbrida

1. **Eficiencia Computacional (C):** El núcleo numérico (las pesadas evaluaciones de $S(q)$ frente a miles de iteraciones con parámetros diferentes) es gestionado por un ejecutable hiper-rápido compilado de lenguaje C.
2. **Capacidad de Navegación (Python):** La metaheurística de Scipy (`scipy.optimize.differential_evolution`) comanda la búsqueda inteligente. Rastrea continuamente a toda su "población" de individuos por el espacio n-dimensional.

## Características

* Ejecución mediante Interfaz de Línea de Comandos (CLI) de fácil uso.
* Compatible de caja con modelos Yukawa y Esferas Duras (HS). Expandible.
* **Top-K Extractor:** No nos conformamos solo con el mínimo global. Extraemos los parámetros de las 3 mejores conjeturas finales de toda la población generacional para dar flexibilidad y alternativas de ajuste al físico.
* Generación visual automática de resultados.

## Instalación

1. **Requisitos:**
   - Un compilador de C estándar (e.g. `gcc`).
   - Python 3.8 o superior con `numpy`, `scipy` y `matplotlib`.

2. **Compilar el Motor C:**
   Puesto que ahora se integra directamente con el motor físico real de ecuaciones integrales de `structures`, requerimos compilar vinculando la librería GSL (GNU Scientific Library).
   ```bash
   mkdir -p build
   gcc -O3 -o build/calcula_Sq core/calcula_Sq.c ../structures/Hard_Sphere/Hard_Sphere.c -I../structures/Hard_Sphere -lm -lgsl -lgslcblas
   ```

## Uso

Para usar la herramienta para ajustar datos propios, asegúrese de tener un archivo `.dat` en formato de dos columnas separadas por espacio: ($q_{exp}$ | $S(q)_{exp}$).

**Comando Estándar:**
```bash
python main.py --input /ruta/al/archivo/datos.dat --modelo yukawa
```

Opciones admitidas:
- `--input`: Ruta obligatoria al archivo con datos.
- `--modelo`: Puede ser `yukawa` o `hs`. (Por omisión `yukawa`).

## Salidas Generadas

1. **Terminal:** Detalles sobre convergencia, costo asociado y el desdoble de parámetros del Top 3 de individuos óptimos encontrados.
2. **Gráficos PNG:** Archivo almacenado localmente con el perfíl continuo de los 3 mejores ajustes sobrepuestos en los puntos experimentales. Útil para revisión expedita de calidad.

# Edi-Bot 🤖
### Evolutionary & Differential Inference-Based Optimization Tool

**Edi-Bot** es una infraestructura de optimización híbrida diseñada para la inferencia de parámetros físicos en sistemas coloidales mediante el ajuste del **Factor de Estructura Estático $S(q)$**. Combina la eficiencia de cálculo de un motor numérico en **C** con la robustez de los algoritmos de **Evolución Diferencial (DE)** y **Particle Swarm Optimization (PSO)** en **Python**.

---

## 🚀 Características Principales
- **Motor Híbrido:** Cálculo de alta velocidad en C (Percurs-Yevick, MSA, Doble Yukawa) integrado con Python.
- **Multi-Algoritmo:** Soporte para **Evolución Diferencial (DE)** y **Particle Swarm Optimization (PSO)** para una exploración robusta.
- **Visualización Diferenciada:** Estilos de gráficas personalizados por algoritmo para una rápida identificación visual en los reportes (Azul/Rojo para DE, Púrpura/Rosa para PSO).
- **Reporteo Automatizado:** Generación de bitácoras académicas en LaTeX con gráficas de alta resolución y tablas comparativas.
- **Ponderación MSE:** Algoritmo ajustable para priorizar la precisión en regiones críticas de bajo vector de onda ($q$ pequeños).

---

## 📋 Requisitos Previos
- **C Compiler:** GCC (Linux/macOS).
- **Librerías C:** [GSL (GNU Scientific Library)](https://www.gnu.org/software/gsl/).
- **Python:** 3.10 o superior.
- **LaTeX:** TeX Live o similar (para generación de reportes en PDF).

---

## 🛠️ Instalación y Compilación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Riperedo/Edi-Bot.git
   cd Edi-Bot
   ```

2. **Compilar el motor numérico en C:**
   ```bash
   mkdir -p sq_optimizer/build
   gcc -O3 sq_optimizer/core/calcula_Sq.c structures/Hard_Sphere/Hard_Sphere.c structures/Hard_Sphere_Double_Yukawa/Hard_Sphere_Double_Yukawa.c -o sq_optimizer/build/calcula_Sq -lgsl -lgslcblas -lm
   ```

3. **Instalar dependencias de Python:**
   ```bash
   pip install numpy scipy matplotlib
   ```

---

## 📖 Guía de Uso

### 1. Workflow Automatizado (Recomendado)
Para procesar un archivo de datos, realizar la optimización y actualizar el reporte LaTeX en un solo paso:
```bash
python3 run_workflow.py Simulation_Data/example_01.dat hs pso
```
*Modelos: `hs`, `hs_vw`, `wca`, `yukawa`, `yukawa_atractivo`, `doble_yukawa`.*
*Algoritmos: `de` (default), `pso`.*

### 2. Herramienta de Consola (Standalone)
```bash
python3 sq_optimizer/main.py --input Simulation_Data/SmAb2:Arg.dat --modelo doble_yukawa --algoritmo pso
```

### 3. Exploración Manual
¿Los resultados automáticos no son satisfactorios? Consulta el tutorial de exploración guiada:
- [EXPLORACION_MANUAL.md](./EXPLORACION_MANUAL.md)

---

## 🏆 Caso de Uso: Optimización Comparativa

Recientemente, Edi-Bot fue utilizado para parametrizar complejos sistemas de Yukawa Doble comparando el rendimiento de DE y PSO en datasets del mundo real:

**Datasets destacados:**
- `SmAb2:Arg.dat`, `SmAb4:arg.dat` (Optimizados con **PSO**)
- `SmAb2:NaCl.dat`, `SmAb4:NaCl.dat` (Optimizados con **DE**)

Este flujo de trabajo permitió identificar que, para estos sistemas específicos, PSO muestra una convergencia más rápida hacia mínimos globales profundos.

---

## 📂 Estructura del Proyecto
- `sq_optimizer/`: Núcleo del optimizador (C y Python Wrappers).
- `structures/`: Librería de funciones físicas de S(q).
- `Simulation_Data/`: Datos experimentales y de simulación.
- `reporte_optimizacion/`: Plantillas y salida del reporte acumulativo LaTeX.
- `run_workflow.py`: Orquestador principal del pipeline.

---

## 🗺️ Hoja de Ruta (Roadmap)
- [ ] Incorporar soluciones numéricas para $S(q)$ y $g(r)$.
- [ ] Paralelización del cálculo de poblaciones.
- [ ] Incorporación de Mezclas Binarias.
- [ ] Interfaz Gráfica (GUI) para visualización en tiempo real.

---

**Edi-Bot** - Desarrollado para la comunidad de física estadística y coloidal. 🧪✨

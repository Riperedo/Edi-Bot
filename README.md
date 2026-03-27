# Edi-Bot 🤖
### Evolutionary & Differential Inference-Based Optimization Tool

**Edi-Bot** es una infraestructura de optimización híbrida diseñada para la inferencia de parámetros físicos en sistemas coloidales mediante el ajuste del **Factor de Estructura Estático $S(q)$**. Combina la eficiencia de cálculo de un motor numérico en **C** con la robustez de los algoritmos de **Evolución Diferencial (DE)** y **Particle Swarm Optimization (PSO)** en **Python**.

---

## 🚀 Características Principales

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
   El proyecto utiliza un script de compilación automática. Desde la raíz:
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
python3 run_workflow.py Simulation_Data/example_01.dat hs
```
*Modelos disponibles: `hs` (Esferas Duras), `yukawa`, `yukawa_atractivo`, `doble_yukawa`.*

### 2. Herramienta de Consola (Standalone)
Si solo deseas realizar el ajuste sin generar el reporte completo de LaTeX:
```bash
python3 sq_optimizer/main.py --input Simulation_Data/SmAb2:Arg.dat --modelo doble_yukawa
```

### 3. Exploración Manual
¿Los resultados automáticos no son satisfactorios? Consulta el tutorial de exploración manual:
- [EXPLORACION_MANUAL.md](./EXPLORACION_MANUAL.md)

---

## 📂 Estructura del Proyecto
- `sq_optimizer/`: Núcleo del optimizador (C y Python Wrappers).
- `structures/`: Librería de funciones físicas de S(q).
- `Simulation_Data/`: Datos experimentales y de simulación de ejemplo.
- `reporte_optimizacion/`: Plantillas y salida del reporte acumulativo.
- `run_workflow.py`: Orquestador principal del pipeline.

---

## 🗺️ Hoja de Ruta (Roadmap)
- [ ] Paralelización del cálculo de poblaciones.
- [ ] Incorporación de modelos WCA y Mezclas Binarias.
- [ ] Interfaz Gráfica (GUI) para visualización en tiempo real.

---

**Edi-Bot** - Desarrollado para la comunidad de física estadística y coloidal. 🧪✨

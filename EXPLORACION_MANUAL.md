# Tutorial: Exploración Manual de Parámetros y Ajuste de S(q)

Este tutorial te guiará para realizar una exploración manual del espacio de parámetros utilizando el motor de cálculo en C y los envoltorios en Python. Esto es especialmente útil cuando la optimización automática (DE) no logra capturar la física fina del sistema o cuando sospechas que los rangos de búsqueda (*bounds*) son inadecuados.

## 1. El Motor de Cálculo (Nivel Bajo)

Si deseas evaluar un único punto en el espacio de parámetros rápidamente, utiliza el binario de C directamente.

### Esferas Duras (HS)
```bash
./sq_optimizer/build/calcula_Sq --model hs --phi 0.1 --sigma 1.0 > evaluacion.dat
```

### Doble Yukawa
```bash
./sq_optimizer/build/calcula_Sq --model doble_yukawa --phi 0.2 --Ta 1.0 --Tr 0.5 --za 5.0 --zr 2.0 --sigma 1.0 > evaluacion.dat
```

*Nota: `evaluacion.dat` contendrá dos columnas: vector de onda (q) y Factor de Estructura (S(q)).*

---

## 2. Exploración Interactiva con Python

Hemos preparado un script para que puedas evaluar el error (MSE) y generar una gráfica comparativa instantánea sin correr el proceso evolutivo completo.

### Paso 1: Localiza tu archivo de datos
Asegúrate de saber la ruta, por ejemplo: `Simulation_Data/150mMNaCl_110mgsmL.dat`.

### Paso 2: Ejecuta la evaluación de prueba
Puedes usar la CLI de `main.py` para visualizar un conjunto específico de parámetros:

```bash
# Ejemplo para Doble Yukawa con parámetros específicos
python3 sq_optimizer/main.py --input Simulation_Data/150mMNaCl_110mgsmL.dat \
                             --model doble_yukawa \
                             --phi 0.1 \
                             --Ta 2.5 \
                             --Tr 0.1 \
                             --za 8.0 \
                             --zr 1.5 \
                             --sigma 1.0
```

Este comando:
1. Llamará al motor en C con esos parámetros exactos.
2. Calculará el MSE (ponderado hacia q pequeñas).
3. **Generará una gráfica automática** llamada `out_doble_yukawa_150mMNaCl_110mgsmL.dat.png` para que compares visualmente.

---

## 3. ¿Cómo "afinar" el ajuste manual?

Si notas que el mínimo de la curva S(q) no coincide (el primer pico), ajusta:
- **`phi`**: Controla la intensidad del empaquetamiento (y por tanto la altura del pico principal).
- **`sigma`**: Desplaza la posición de todos los picos en el eje $q$.
- **`za` / `zr`**: Controlan el alcance de la atracción/repulsión. Un valor pequeño de $z$ significa interacción de largo alcance.
- **`Ta` / `Tr`**: Intensidad de las colas de interacción.

### Estrategia recomendada:
1. Inicia con un valor de `phi` razonable (estimado del experimento).
2. Ajusta `sigma` hasta que el primer pico coincida en posición.
3. Juega con `Ta` y `za` para ajustar la forma de la "subida" a q pequeñas.

---

## 4. Modificar los Rangos de Búsqueda (Bounds)

Si prefieres que la computadora siga intentándolo pero en una región más estrecha que tú ya identificaste, modifica el archivo `sq_optimizer/main.py`:

```python
# Busca esta sección en main.py (línea ~104)
elif model_name == "doble_yukawa":
    param_names = ['phi', 'Ta', 'Tr', 'za', 'zr', 'sigma']
    # Cambia estos valores por tus nuevas sospechas
    bounds = [(0.05, 0.15), (2.0, 3.0), (0.0, 0.5), (7.0, 9.0), (1.0, 2.0), (0.8, 1.2)]
```

Luego vuelve a correr el workflow:
```bash
python3 run_workflow.py Simulation_Data/150mMNaCl_110mgsmL.dat doble_yukawa
```

Esto generará el reporte en LaTeX con la nueva exploración "guiada".

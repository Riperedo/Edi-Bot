# Fases de desarrollo

## Fase 1: Adaptación de la Paquetería en C (El Motor Calculador)

El objetivo aquí es asegurar que tu programa en C funcione estrictamente como un "esclavo" de cálculo sin interfaces interactivas, leyendo los q exactos que Python le mande.

* Paso 1.1: Modificar la entrada de q. Tu programa en C debe ser capaz de leer un archivo de texto (generado por Python) que contenga la columna de datos experimentales q.

* Paso 1.2: Ajustar la recepción de parámetros. El ejecutable debe recibir por línea de comandos los parámetros físicos del modelo elegido y el factor de escala σ para el vector de onda q. Por ejemplo: ./calcula_Sq --modelo yukawa --phi 0.15 --carga 3.2 --sigma 50.0 --input q_exp.txt

* Paso 1.3: Estandarizar la salida. El programa de C debe imprimir en la terminal (o guardar en un archivo de salida) únicamente la columna de valores calculados S(q) correspondientes, sin texto adicional (nada de "Calculando...", "Proceso terminado", etc.).

## Fase 2: El Puente Python-C (El Wrapper)

Python actuará como el controlador que orquesta el envío de datos y la recolección de resultados.

* Paso 2.1: Función de lectura de datos experimentales. Escribir un script usando numpy o pandas que lea los archivos de la literatura (.dat) y separe los vectores q_exp​ y S(q)_exp​.

* Paso 2.2: Función de ejecución (subprocess). Crear una función en Python que tome el vector q_exp​ y un arreglo de parámetros (propuestos por el algoritmo), guarde temporalmente q_exp​ en un .dat, construya el comando de terminal y ejecute tu binario de C.

* Paso 2.3: Captura de resultados. La misma función debe leer la salida del programa en C y convertirla en un arreglo de numpy que contenga el S(q)_calc​.

## Fase 3: Construcción de la Función Objetivo (Fitness)

Esta es la brújula que guiará a la Evolución Diferencial.

* Paso 3.1: Empaquetar el modelo. Crear una función genérica objetivo(parametros, q_exp, Sq_exp). El arreglo parametros incluirá todos los valores físicos más el factor σ.

* Paso 3.2: Evaluar y comparar. Dentro de esa función, se llamará al wrapper del Paso 2.2 pasándole q_exp y parametros.

* Paso 3.3: Calcular la métrica de error. La función retornará la suma de los residuos al cuadrado:
    Error=∑(S(q)exp​−S(q)calc​)2

## Fase 4: El Motor de Optimización Híbrida

Aquí implementamos la inteligencia matemática para encontrar los mejores parámetros.

* Paso 4.1: Definir los límites (Bounds). Crear una lista de rangos máximos y mínimos físicos para cada parámetro, incluyendo σ (ej. ϕ∈[0.01,0.74]).

* Paso 4.2: Evolución Diferencial (Búsqueda Global). Alimentar la función objetivo y los límites a scipy.optimize.differential_evolution. El algoritmo explorará el espacio y encontrará la región del mínimo global, evitando atorarse en mínimos locales.

* Paso 4.3: Pulido Local (Opcional pero recomendado). Usar el mejor resultado de la Evolución Diferencial como punto de partida inicial para un algoritmo basado en gradientes (como scipy.optimize.least_squares). Esto refinará los decimales y te dará el ajuste perfecto mucho más rápido que dejar que la Evolución Diferencial converja sola hasta el final.

## Fase 5: Automatización por Lotes y Resultados

Finalmente, empaquetamos todo para que puedas procesar decenas de datasets automáticamente.

* Paso 5.1: Bucle de procesamiento. Escribir un bucle que itere sobre una carpeta llena de archivos experimentales, aplique las Fases 2 a 4 para cada uno, y guarde los parámetros óptimos encontrados en un archivo resumen (un dat maestro).

* Paso 5.2: Visualización. Usar matplotlib para generar automáticamente y guardar una gráfica por cada dataset, superponiendo los puntos experimentales S(q)exp​ y la línea continua de tu mejor ajuste S(q)calc​ (Para la S(q)calc se deberan usar mas puntos de grid, por ejemplo 1000 puntos en entre el minimo de q_exp y el maximo de q_exp). Esto te permite hacer una inspección visual de control de calidad al final del día.


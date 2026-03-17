# Plan de desarrollo Particle Swarn Optimization

## Fase 1: El Puente Python-C (La Base Intacta)

El núcleo computacional en C se mantiene exactamente igual.

* Paso 1.1: Python escribe el vector de datos q_exp​ en un archivo temporal de texto.

* Paso 1.2: Python usa subprocess para llamar a tu binario en C, enviándole la ruta de q_exp​, los parámetros del modelo y el factor de escala σ.

* Paso 1.3: El programa en C imprime o guarda los valores de S(q)calc​, y Python los lee en un arreglo de numpy.

## Fase 2: La Función de Costo "Vectorizada"

Aquí es donde adaptamos el puente para el enjambre.

* Paso 2.1: Crear una función calcular_costo_particula(parametros). Esta es la función individual que llama a tu puente (Fase 1) para una sola partícula y devuelve el Error Cuadrático Medio (MSE) frente a S(q)exp​.

* Paso 2.2: Crear la función "envoltura" para el enjambre: funcion_objetivo_enjambre(matriz_particulas). La librería pyswarms le pasará a esta función una matriz donde cada fila es una partícula.

* Paso 2.3: Dentro de esta envoltura, debes programar un bucle (o usar paralelismo en Python con multiprocessing) que iterativamente tome cada fila, llame a calcular_costo_particula y guarde el error. La función debe retornar un arreglo unidimensional con los errores de todas las partículas de esa iteración.

## Fase 3: Configuración del Enjambre (La Física del Algoritmo)

A diferencia de la Evolución Diferencial, PSO tiene parámetros que simulan leyes físicas para controlar el vuelo de las partículas.

* Paso 3.1: Definir Límites (Bounds). En pyswarms, esto se hace creando dos arreglos (tuplas): uno con los límites mínimos de todos los parámetros y otro con los máximos (incluyendo σ).

* Paso 3.2: Ajustar la "Física" (Hiperparámetros). Debes definir un diccionario con tres valores fundamentales:

* w (Inercia): Qué tanto tiende la partícula a seguir su rumbo actual.

    [1] c1​ (Parámetro cognitivo): Qué tanto le atrae su propio mejor descubrimiento histórico.

    [2] c2​ (Parámetro social): Qué tanto le atrae el mejor descubrimiento de todo el enjambre.

* Paso 3.3: Instanciar y Ejecutar. Creas el optimizador pyswarms.single.GlobalBestPSO indicando el número de partículas, las dimensiones (cantidad de parámetros), los límites y la "física". Luego, inicias el vuelo llamando al método optimize.

## Fase 4: Análisis y Automatización

PSO te ofrece herramientas de diagnóstico muy intuitivas sobre cómo se comportó el enjambre.

* Paso 4.1: Extracción del Óptimo. El algoritmo te devolverá el mejor costo alcanzado y el vector de parámetros óptimo.

* Paso 4.2: Gráfico de Costo. Usar pyswarms.utils.plotters.plot_cost_history para ver cómo disminuyó el error con cada generación. Si la curva baja muy rápido y se estanca, podrías necesitar aumentar la inercia w para explorar más.

* Paso 4.3: Automatización por lotes. Como en los planes anteriores, envuelves todo esto en un script que itere sobre tus diferentes archivos de datos experimentales, optimice cada uno y guarde los parámetros finales junto con un gráfico superponiendo S(q)exp​ y S(q)calc​.

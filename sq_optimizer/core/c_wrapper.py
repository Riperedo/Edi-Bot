import subprocess
import tempfile
import os
import numpy as np

# Ruta al ejecutable de C compilado
C_EXECUTABLE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build", "calcula_Sq")

def evaluate_sq_c(q_exp, params_dict):
    """
    Función wrapper que envía el vector q a C, pasa los parámetros por línea
    de comando, ejecuta el binario y captura la respuesta S(q)_calc.
    
    :param q_exp: np.ndarray del vector de magnitudes q experimentales
    :param params_dict: Diccionario con los parámetros, e.g.
                        {'modelo': 'yukawa', 'phi': 0.1, 'carga': 3.0, 'sigma': 1.0}
    :return: np.ndarray del S(q)_calc evaluado por el programa en C
    """
    if not os.path.exists(C_EXECUTABLE_PATH):
        raise FileNotFoundError(f"No se encontró el ejecutable C en: {C_EXECUTABLE_PATH}")

    # Escribir los datos q temporalmente a un archivo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        for q in q_exp:
            tmp_file.write(f"{q}\n")
        temp_input_path = tmp_file.name

    try:
        # Construir el comando con argumentos de línea
        cmd = [C_EXECUTABLE_PATH, "--input", temp_input_path]
        
        # Añadir todos los parámetros dinámicamente
        if 'modelo' in params_dict:
            cmd.extend(["--modelo", str(params_dict['modelo'])])
        if 'phi' in params_dict:
            cmd.extend(["--phi", str(params_dict['phi'])])
        if 'carga' in params_dict:
            cmd.extend(["--carga", str(params_dict['carga'])])
        if 'sigma' in params_dict:
            cmd.extend(["--sigma", str(params_dict['sigma'])])

        if 'Ta' in params_dict:
            cmd.extend(["--Ta", str(params_dict['Ta'])])
        if 'Tr' in params_dict:
            cmd.extend(["--Tr", str(params_dict['Tr'])])
        if 'za' in params_dict:
            cmd.extend(["--za", str(params_dict['za'])])

        # Ejecutar el subproceso
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parsear la salida estándar
        output_lines = result.stdout.strip().split('\n')
        sq_calc = np.array([float(line) for line in output_lines if line.strip()])
        
        # Checkeo de consistencia: debe regresar mismo número de puntos
        if len(sq_calc) != len(q_exp):
            raise ValueError(f"Dimensión mismatch: C devolvió {len(sq_calc)} valores, esperado {len(q_exp)}")
            
        return sq_calc

    except subprocess.CalledProcessError as e:
        print(f"Error en la llamada a C:\n{e.stderr}")
        raise e
    finally:
        # Siempre limpiar el archivo temporal
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)


def cost_function(params_array, param_names, q_exp, sq_exp, model_name="yukawa"):
    """
    Función de costo general que usa Differential Evolution para calcular
    el (Mean Squared Error).
    
    :param params_array: Array 1D de parámetros sugeridos por Differential Evolution
    :param param_names: Lista de nombres, ej: ['phi', 'carga', 'sigma']
    :param q_exp: np.ndarray con q experimentales
    :param sq_exp: np.ndarray con S(q) experimentales
    :param model_name: Nombre del modelo para C ('yukawa' o 'hs')
    :return: float, el error residual
    """
    # Mapear el array sin nombre de Scipy a un diccionario de entrada
    params_dict = {'modelo': model_name, 'sigma': 1.0}
    for name, val in zip(param_names, params_array):
        params_dict[name] = val
        
    sq_calc = evaluate_sq_c(q_exp, params_dict)
    
    # Calcular residuo (Weighted Mean Squared Error) ponderando más los q pequeños
    # Usamos un peso que decae con q, por ejemplo: 1 / (q_exp + 0.1)^2
    weights = 1.0 #/ (q_exp + 0.1)**2
    # Normalizamos los pesos para no disparar la magnitud del costo global
    weights = weights / np.mean(weights)
    
    error = np.mean(weights * (sq_exp - sq_calc)**2)
    return error

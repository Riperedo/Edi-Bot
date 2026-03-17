import argparse
import os
import sys
import numpy as np

# Aseguramos que el core está en el path (necesario al ejecutar independientemente)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.c_wrapper import evaluate_sq_c
from core.optimize_de import run_de_optimizer
from utils.plot_results import save_top_k_plot

def process_file(file_path, model_name):
    print(f"\n>>>> Procesando: {os.path.basename(file_path)}")
    try:
        # Cargar datos experimentales: asuminos dos columnas: q y S(q)
        data = np.loadtxt(file_path)
        q_exp = data[:, 0]
        sq_exp = data[:, 1]
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return
        
    # Definir modelos y límites (Limites fisicos aproximados)
    if model_name == "yukawa":
        param_names = ['phi', 'carga', 'sigma']
        bounds = [(0.01, 0.6), (1.0, 10.0), (0.5, 1.5)] 
    elif model_name == "hs":
        param_names = ['phi', 'sigma']
        bounds = [(0.01, 0.6), (0.5, 1.5)]
    elif model_name == "yukawa_atractivo":
        param_names = ['phi', 'Ta', 'za', 'sigma']
        bounds = [(0.01, 0.6), (0.1, 5.0), (0.1, 10.0), (0.5, 1.5)]
    elif model_name == "doble_yukawa":
        param_names = ['phi', 'Ta', 'Tr', 'za', 'zr', 'sigma']
        bounds = [(0.01, 0.6), (0.1, 5.0), (0.1, 5.0), (0.1, 10.0), (0.1, 10.0), (0.5, 20.0)]
    elif model_name == "hs_vw":
        param_names = ['phi', 'sigma']
        bounds = [(0.01, 0.6), (0.5, 1.5)]
    elif model_name == "wca":
        param_names = ['phi', 'Tf', 'sigma']
        bounds = [(0.01, 0.6), (0.1, 5.0), (0.5, 1.5)]
    else:
        print(f"Modelo {model_name} no reconocido.")
        return

    # Ejecutar la busqueda DE
    results = run_de_optimizer(q_exp, sq_exp, param_names, bounds, model_name=model_name, top_k=3, maxiter=25)
    
    print("\n[RESULTADOS]")
    print(f"Status DE Converge: {results['success']} tras evaluacion de coste {results['nfev']} veces")
    
    for i in range(3):
        print(f"Top {i+1} Vector: [", ", ".join([f"{n}={v:.3f}" for n,v in zip(param_names, results['top_k_params'][i])]), f"] -> Error: {results['top_k_costs'][i]:.5f}")

    # Guardar grafica
    out_img = f"out_{model_name}_{os.path.basename(file_path)}.png"
    save_top_k_plot(q_exp, sq_exp, results['top_k_params'], param_names, model_name, out_img)
    print(f"Graica de resultados guardada en {out_img}")

def main():
    parser = argparse.ArgumentParser(description="Optimizador de S(q) Coloidal - CLI Independiente")
    parser.add_argument("--input", required=True, help="Ruta al archivo .dat experimental de entrada.")
    parser.add_argument("--modelo", default="yukawa", choices=["yukawa", "hs", "yukawa_atractivo", "doble_yukawa", "hs_vw", "wca"], help="Modelo a utilizar.")
    args = parser.parse_args()

    # Comprobar la existencia del archivo
    if not os.path.isfile(args.input):
        print(f"Error: Archivo de entrada {args.input} no existe.")
        sys.exit(1)

    process_file(args.input, args.modelo)

if __name__ == "__main__":
    main()

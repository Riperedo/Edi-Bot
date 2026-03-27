import argparse
import os
import sys
import numpy as np

# Aseguramos que el core está en el path (necesario al ejecutar independientemente)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.c_wrapper import evaluate_sq_c
from core.optimize_de import run_de_optimizer
from core.particle_swarm import run_pso_optimizer
from utils.plot_results import save_top_k_plot

def process_file(file_path, model_name, algoritmo="de", maxiter=25):
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

    # Ejecutar la búsqueda
    if algoritmo == "de":
        results = run_de_optimizer(q_exp, sq_exp, param_names, bounds, model_name=model_name, top_k=3, maxiter=maxiter)
    elif algoritmo == "pso":
        results = run_pso_optimizer(q_exp, sq_exp, param_names, bounds, model_name=model_name, top_k=3, maxiter=maxiter)
    else:
        print(f"Algoritmo {algoritmo} no reconocido.")
        return
    
    print("\n[RESULTADOS]")
    print(f"Status {algoritmo.upper()} Converge: {results['success']} tras evaluacion de coste {results['nfev']} veces")
    
    for i in range(len(results['top_k_params'])):
        print(f"Top {i+1} Vector: [", ", ".join([f"{n}={v:.3f}" for n,v in zip(param_names, results['top_k_params'][i])]), f"] -> Error: {results['top_k_costs'][i]:.5f}")

    # Guardar grafica
    out_img = f"out_{model_name}_{os.path.basename(file_path)}.png"
    save_top_k_plot(q_exp, sq_exp, results['top_k_params'], param_names, model_name, out_img)
    print(f"Gráfica de resultados guardada en {out_img}")

def main():
    parser = argparse.ArgumentParser(description="Optimizador de S(q) Coloidal - CLI Independiente")
    parser.add_argument("--input", required=True, help="Ruta al archivo .dat experimental de entrada.")
    parser.add_argument("--modelo", default="yukawa", choices=["yukawa", "hs", "yukawa_atractivo", "doble_yukawa", "hs_vw", "wca"], help="Modelo a utilizar.")
    parser.add_argument("--algoritmo", default="de", choices=["de", "pso"], help="Algoritmo de optimización (default: de).")
    parser.add_argument("--maxiter", type=int, default=25, help="Iteraciones máximas.")
    args = parser.parse_args()

    # Comprobar la existencia del archivo
    if not os.path.isfile(args.input):
        print(f"Error: Archivo de entrada {args.input} no existe.")
        sys.exit(1)

    process_file(args.input, args.modelo, algoritmo=args.algoritmo, maxiter=args.maxiter)

if __name__ == "__main__":
    main()

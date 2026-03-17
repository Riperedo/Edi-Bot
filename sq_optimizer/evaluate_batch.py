import os
import glob
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import process_file

def evaluate_directory(data_dir, model_name="yukawa"):
    """
    Busca todos los archivos .dat en el directorio especificado 
    y ejecuta la optimizacion DE sobre ellos.
    """
    print(f"=== BATCH EVALUATION STARTS ({model_name.upper()}) ===")
    
    # Buscar todos los archivos .dat
    search_pattern = os.path.join(data_dir, "*.dat")
    dat_files = sorted(glob.glob(search_pattern))
    
    if not dat_files:
        print(f"No se encontraron archivos en: {data_dir}")
        return

    print(f"Archivos encontrados: {len(dat_files)}")
    
    t0 = time.time()
    for file_path in dat_files:
        try:
            # Ejecutamos el pipeline de la herramienta standalone
            process_file(file_path, model_name)
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            
    tf = time.time()
    print(f"\n=== EVALUATOR BATCH FINISHED ===")
    print(f"Tiempo Total: {tf - t0:.2f} segundos")

if __name__ == "__main__":
    # Apuntamos a la carpeta de validación del proyecto
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Simulation_Data"))
    model = sys.argv[1] if len(sys.argv) > 1 else "yukawa"
    evaluate_directory(target_dir, model_name=model)

import os
import sys
import shutil
import time
import subprocess
import re

# Añadir sq_optimizer al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "sq_optimizer")))

from sq_optimizer.core.optimize_de import run_de_optimizer
import numpy as np
from sq_optimizer.utils.plot_results import save_top_k_plot

def inject_latex(tex_path, top_params, top_costs, param_names, img_path, model_name="yukawa", bounds=[], target_file=""):
    """
    Substituye placeholders en el archivo LaTeX para automatizar dinamicamente el reporte.
    """
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reemplazar nombre del modelo
    content = re.sub(r'%%MODELO_NAME%%', model_name.upper(), content)

    # 1. Inyectar valores de tabla
    # Construir cabecera dinámica
    header = " & ".join([f"\\textbf{{{name}}}" for name in param_names])
    table_replacement = f"""\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{{'c' * (len(param_names) + 2)}}}
\\toprule
\\textbf{{Rango}} & {header} & \\textbf{{Costo (MSE)}} \\\\
\\midrule
"""
    for i in range(min(3, len(top_params))):
        vals_str = " & ".join([f"{val:.3f}" for val in top_params[i]])
        table_replacement += f"Top {i+1} & {vals_str} & {top_costs[i]:.5f} \\\\\n"
    
    table_replacement += """\\bottomrule
\\end{tabular}
\\caption{Parámetros top 3 obtenidos de la evolución paramétrica de DE para este dataset.}
\\end{table}"""
    
    # 2. Inyectar imagen
    image_name = os.path.basename(img_path)
    image_replacement = f"""\\begin{{figure}}[h!]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{image_name}}}
\\caption{{Ajuste de los datos originales frente al top 3 continuo.}}
\\end{{figure}}"""


    bounds_str = ", ".join([f"{name} $\\in$ [{b[0]}, {b[1]}]" for name, b in zip(param_names, bounds)])
    
    base_name = os.path.basename(img_path).replace("plot_workflow_", "").replace(".png", "")
    new_section = f"""\\subsection*{{Resultados para {base_name.replace('_', '\\_')} (Modelo {model_name.upper()})}}
\\textbf{{¿Cómo replicar?}} Ejecute el siguiente comando en la terminal desde el directorio raíz del pipeline:
\\begin{{verbatim}}
python sq_optimizer/main.py --input {target_file} --model {model_name}
\\end{{verbatim}}
\\textbf{{Límites de Búsqueda (Bounds):}} Los parámetros variables fueron explorados por Differential Evolution dentro de los siguientes radios de tolerancia físicos dictados: \\newline
{bounds_str}
\\vspace{{0.4cm}}

{table_replacement}
{image_replacement}
\\vspace{{0.5cm}}
\\hrule
\\vspace{{0.5cm}}
"""
    
    content = content.replace("%%APPEND_RESULTS_HERE%%", f"{new_section}\n%%APPEND_RESULTS_HERE%%")

    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(content)

def run_workflow(target_file, model_name="yukawa"):
    print(f"\n>>>> INICIANDO WORKFLOW AUTOMÁTICO EN {target_file}")
    
    # Check
    if not os.path.isfile(target_file):
        print("Archivo no válido.")
        return

    # 1. Optimizar datos cargados
    print("[1/3] Ejecutando Optimización Numérica...")
    try:
        data = np.loadtxt(target_file)
        q_exp = data[:, 0]
        sq_exp = data[:, 1]
    except Exception as e:
        print(f"Error parseando archivo: {e}")
        return
        
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
        bounds = [(0.01, 0.3), (0.1, 5.0), (0.1, 5.0), (0.01, 10.0), (0.01, 10.0), (53.0, 56.0)]

    results = run_de_optimizer(q_exp, sq_exp, param_names, bounds, model_name=model_name, top_k=3, maxiter=25)
    
    # 2. Generar y mover gráfica al directorio de LaTeX
    print("[2/3] Generando Artefactos Analíticos (Gráficas)...")
    tex_dir = os.path.join(os.path.dirname(__file__), "reporte_optimizacion")
    out_img_name = f"plot_workflow_{os.path.basename(target_file)}.png"
    out_img_path = os.path.join(tex_dir, out_img_name)
    
    save_top_k_plot(q_exp, sq_exp, results['top_k_params'], param_names, model_name, out_img_path)

    # 3. Compilar LaTeX
    print("[3/3] Compilando Documento Formal en LaTeX...")
    tex_dir = os.path.join(os.path.dirname(__file__), "reporte_optimizacion")
    tex_file = os.path.join(tex_dir, "main.tex")
    
    inject_latex(tex_file, results['top_k_params'], results['top_k_costs'], param_names, out_img_path, model_name=model_name, bounds=bounds, target_file=target_file)

    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=tex_dir, check=True, stdout=subprocess.DEVNULL)
        print("\n=== WORKFLOW CONCLUÍDO SATISFACTORIAMENTE ===")
        print(f"Reporte exportado como PDF: {os.path.join(tex_dir, 'main.pdf')}")
    except FileNotFoundError:
        print("Error: pdflatex no encontrado. Instale textlive para compilar el pdf, pero el .tex fue actualizado perfectamente.")
    except subprocess.CalledProcessError:
        print("Avisos levantados durante la compilación, pero el PDF probablemente fue generado. Revise la carpeta reporte_optimizacion.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run_workflow.py <Simulation_Data/nuevo_ejemplo.dat> [modelo]")
    else:
        model = sys.argv[2] if len(sys.argv) > 2 else "yukawa"
        run_workflow(sys.argv[1], model_name=model)

import matplotlib.pyplot as plt
import numpy as np

def save_top_k_plot(q_exp, sq_exp, top_k_params, param_names, model_name, output_path):
    """
    Genera una grafica superponiendo los datos discretos experimentales 
    con las curvas continuas del Top-K encontradas.
    """
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.c_wrapper import evaluate_sq_c
    
    plt.figure(figsize=(10, 6))
    
    # Grafica de datos experimentales originales (Puntos discretos negros)
    plt.plot(q_exp, sq_exp, 'ko', markersize=4, label='S(q) Experimental', alpha=0.7)
    
    # Colores visualmente agradables y definidos
    colors = ['#e63946', '#457b9d', '#2a9d8f', '#f4a261', '#e9c46a']
    
    # Generar un grid más fino para trazar curvas suaves, usando el dominio original
    q_dense = np.linspace(min(q_exp), max(q_exp), num=1000)
    
    # Dibujar cada una de las soluciones del Top-K
    for i, params_array in enumerate(top_k_params):
        # Repack array de valores devuelta al diccionario requerido por c_wrapper
        params_dict = {'modelo': model_name}
        lbl_parts = []
        for name, val in zip(param_names, params_array):
            params_dict[name] = val
            lbl_parts.append(f"{name}={val:.2f}")
            
        lbl = f"Top {i+1} [" + ", ".join(lbl_parts) + "]"
        
        # Evaluar curva densa
        sq_dense = evaluate_sq_c(q_dense, params_dict)
        
        plt.plot(q_dense, sq_dense, color=colors[i % len(colors)], linewidth=2, label=lbl, alpha=0.9 if i==0 else 0.6)
        
    plt.title(f"Ajustes Optimizados {model_name.upper()} (Top {len(top_k_params)}) via DE")
    plt.xlabel('q (Vector de Onda)', fontsize=12)
    plt.ylabel('S(q) (Factor de Estructura)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='lower right')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300)
    plt.close()

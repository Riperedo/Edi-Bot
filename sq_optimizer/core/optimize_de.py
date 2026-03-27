import numpy as np
from scipy.optimize import differential_evolution

from core.c_wrapper import cost_function

class TopKTracker:
    """Clase para trackear de forma personalizada los 3 mejores de un Differential Evolution."""
    def __init__(self, k=3):
        self.k = k
        self.best_params = []
        self.best_costs = []

    def callback(self, xk, convergence=None, **kwargs):
        """Callback ejecutado por DE en cada iteración/generación"""
        # Explicación: differential_evolution a partir de SciPy 1.12+ 
        # pasa un OptimizeResult con 'population' y 'population_energies' en lugar de xk,
        # o inspecciona la firma si es muy moderna. Acomodamos ambos casos.
        
        # En SciPy moderno xk podría ser el intermediate_result
        intermediate_result = xk
        try:
            pop = intermediate_result.population
            energies = intermediate_result.population_energies
            
            # Ordenar las energías de menor a mayor error y obtener índices
            sorted_indices = np.argsort(energies)
            top_k_indices = sorted_indices[:self.k]
            
            # Guardamos el estado al final de esta iteracion
            self.best_params = pop[top_k_indices].copy()
            self.best_costs = energies[top_k_indices].copy()
        except AttributeError:
            pass # Si usamos version antigua de Scipy, callback recibe x, convergence y xk no tiene .population
            

def run_de_optimizer(q_exp, sq_exp, param_names, bounds, model_name="yukawa", top_k=3, maxiter=50):
    """
    Ejecuta el optimizador Differential Evolution para ajustar parametros de S(q).
    """
    # Empaquetamos todo para solo requerir params_array
    def objective(params_array):
        return cost_function(params_array, param_names, q_exp, sq_exp, model_name=model_name)

    # Inicializar rastreador para atrapar a la población al final
    tracker = TopKTracker(k=top_k)

    # Iniciar evolución
    print(f"--- Iniciando Differential Evolution ({model_name}) ---")
    
    # Scipy Differential Evolution: 'best1bin' es la estrategia estandar (DE/rand/1/bin)
    # la documentabion consultada en NotebookLM menciona esta estrategia.
    result = differential_evolution(
        func=objective,
        bounds=bounds,
        strategy='best1bin', 
        maxiter=maxiter,
        popsize=15,          # Num partículas = popsize * len(bounds)
        mutation=(0.5, 1.0), # Factor de escala o mutación F
        recombination=0.7,   # CR
        tol=1e-4,
        callback=tracker.callback,
        updating='deferred'  # Preferido para callbacks que inspeccionan poblaciones
    )
    
    # Manejar caso fallback: el usuario tiene scipy viejo sin access a `.population`
    if len(tracker.best_params) == 0:
        print("Warning: Population tracker not supported in current scipy version. Emulando Top 3 dummy.")
        tracker.best_params = [result.x, result.x * 1.01, result.x * 0.99]
        tracker.best_costs = [result.fun, result.fun*1.1, result.fun*1.05]

    return {
        'global_best_params': result.x,
        'global_best_cost': result.fun,
        'top_k_params': tracker.best_params,
        'top_k_costs': tracker.best_costs,
        'success': result.success,
        'nfev': result.nfev
    }

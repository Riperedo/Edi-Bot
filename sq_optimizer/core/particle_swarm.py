### Modulo de Particle Swarm Optimization (PSO)

import numpy as np
from sq_optimizer.core.c_wrapper import cost_function

def run_pso_optimizer(q_exp, sq_exp, param_names, bounds, model_name="yukawa", top_k=3, maxiter=50, N_particles=50):
    """
    Ejecuta el optimizador Particle Swarm Optimization para ajustar parametros de S(q).
    """
    print(f"--- Iniciando Particle Swarm Optimization ({model_name}) ---")
    
    # Dimensiones
    D = len(bounds)
    bounds_arr = np.array(bounds)
    minimos = bounds_arr[:, 0]
    maximos = bounds_arr[:, 1]
    rango = maximos - minimos

    # posiciones iniciales
    X = np.random.uniform(low=minimos, high=maximos, size=(N_particles, D))

    # velocidades iniciales (10% del rango)
    V = np.random.uniform(low=-rango*0.1, high=rango*0.1, size=(N_particles, D))

    # lista de los pbest
    pbest = X.copy()
    pbest_score = np.full(N_particles, np.inf)

    # mejor resultado global
    gbest_pos = np.zeros(D)
    gbest_score = np.inf

    # Parametros de PSO
    w = 0.5  # inercia
    c1 = 1.5 # cognitivo
    c2 = 1.5 # social

    # Para trackear la recoleccion del fitness
    nfev = 0

    terminar_busqueda = False
    
    for i in range(maxiter):
        for p in range(N_particles):
            # Evaluamos la funcion de costo para la particula p
            # llamando la funcion que internamente llama a C
            score = cost_function(X[p], param_names, q_exp, sq_exp, model_name=model_name)
            nfev += 1

            # Actualizamos pbest
            if score < pbest_score[p]:
                pbest_score[p] = score
                pbest[p] = X[p].copy()

            # Actualizamos gbest
            if score < gbest_score:
                gbest_score = score
                gbest_pos = X[p].copy()
            elif score == gbest_score:
                terminar_busqueda = True
                break
        
        if terminar_busqueda:
            print("Se ha alcanzado el mejor resultado posible.")
            break

        # Imprimir progreso cada 10 iteraciones
        if (i + 1) % 50 == 0 or i == 0:
            print(f"Iteración {i+1}/{maxiter} - Mejor costo (MSE): {gbest_score:.6f}")
                
        # Actualizamos velocidades y posiciones
        r1 = np.random.rand(N_particles, D)
        r2 = np.random.rand(N_particles, D)
        
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest_pos - X)
        X = X + V
        
        # Aplicamos limites iterando sobre particulas o de forma vectorizada
        X = np.clip(X, minimos, maximos)
        
    # Obtener los top k de los pbests para reportarlos
    sorted_indices = np.argsort(pbest_score)
    top_k_indices = sorted_indices[:top_k]
    
    best_params_k = pbest[top_k_indices].copy()
    best_costs_k = pbest_score[top_k_indices].copy()

    

    return {
        'global_best_params': gbest_pos,
        'global_best_cost': gbest_score,
        'top_k_params': best_params_k,
        'top_k_costs': best_costs_k,
        'success': True,
        'nfev': nfev
    }
    
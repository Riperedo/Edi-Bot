import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "sq_optimizer"))
from sq_optimizer.core.c_wrapper import evaluate_sq_c, cost_function

# Cargar los datos experimentales
data = np.loadtxt("Simulation_Data/example_01.dat")
q_exp = data[:, 0]
sq_exp = data[:, 1]

# Parámetros conocidos
phi_val = 0.1
# sigma_val = 1.0 (ya está fijo en c_wrapper.py internamente)

params_dict = {'modelo': 'hs', 'phi': phi_val, 'sigma': 1.0}
sq_calc = evaluate_sq_c(q_exp, params_dict)

# Calcular MSE manualmente para comparar
mse = np.mean((sq_exp - sq_calc)**2)

print(f"Evaluación Manual Hacia C (Modelo HS)")
print(f"Parametros: phi={phi_val}, sigma=1.0")
print(f"MSE Obtenido: {mse:.6f}")

# Imprimir una pequeña muestra de ambos vectores
print("\nMuestra q_exp | sq_exp | sq_calc")
for i in range(10):
    print(f"{q_exp[i]:.4f} | {sq_exp[i]:.4f} | {sq_calc[i]:.4f}")

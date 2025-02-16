#Automatic creation of an virtual environment to run the script and intall the libraries
import subprocess
import os
import venv
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
env_name = os.path.join(script_dir, "VirtualEnv")
if os.path.exists(os.path.join(script_dir, "VirtualEnv")):
    #Checks if the VirtualEnv is activated (This is the path to the Python installation currently in use. If the virtual environment is active, sys.prefix will point to the virtual environment directory, while sys.base_prefix points to the global Python installation.)
    if sys.prefix == sys.base_prefix:
        print("Activating the Virtual Environment...")
        python_exe = os.path.join(env_name, "Scripts", "python")
        subprocess.run([python_exe, __file__])
else:
    print("Installing the Required Libraries on a New Virtual Environment")
    venv.create(env_name, with_pip=True)

    # Step 2: Install the libraries
    libraries = ["scipy","numpy"]
    for lib in libraries:
        subprocess.run([os.path.join(env_name, "Scripts", "pip"), "install", lib], check=True)
    
    #Re-Run the script with the Virtual Env Activated
    python_exe = os.path.join(env_name, "Scripts", "python")
    subprocess.run([python_exe, __file__])





from scipy.optimize import linprog

# Tiempos de cruce
T = {
    ('A', 'J'): 2,
    ('A', 'N'): 5,
    ('A', 'K'): 10,
    ('J', 'N'): 5,
    ('J', 'K'): 10,
    ('N', 'K'): 10,
}

# Variables de decisión (x_AJ, x_AN, ..., r_A, r_J, r_N, r_K)
num_variables = len(T) + 4  # 6 combinaciones de cruces + 4 regresos
c = [T[('A', 'J')], T[('A', 'N')], T[('A', 'K')],
     T[('J', 'N')], T[('J', 'K')], T[('N', 'K')],
     1, 2, 5, 10]  # Coeficientes de la función objetivo

# Restricciones de igualdad (viajes y regresos)
#   AJ AN AK JN JK NK RA RJ RN RK
A_eq = [
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # Suma de cruces = 3
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # Suma de regresos = 2
    [1, 1, 1, 0, 0, 0, -1, 0, 0, 0],  # Stay de A: x_AJ + x_AN + x_AK - r_A = 1
    [1, 0, 0, 1, 1, 0, 0, -1, 0, 0],  # Stay de J: x_AJ + x_JN + x_JK - r_J = 1
    [0, 1, 0, 1, 0, 1, 0, 0, -1, 0],  # Stay de N: x_AN + x_JN + x_NK - r_N = 1
    [0, 0, 1, 0, 1, 1, 0, 0, 0, -1],  # Stay de K: x_AK + x_JK + x_NK - r_K = 1
]
b_eq = [3, 2, 1, 1, 1, 1]

# Bounds para las variables (0 <= x_ij <= , 0 <= r_i <= 2)
bounds = [(0, 3)] * len(T) + [(0, 2)] * 4

# Resolver el problema
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Mostrar resultados
if res.success:
    print("Solución encontrada:")
    print("Valores de las variables:", res.x)
    print("Tiempo total mínimo:", res.fun)
else:
    print("No se encontró solución.")
input("Press any key to Exit")

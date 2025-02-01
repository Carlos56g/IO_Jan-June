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
    libraries = ["scipy"]
    for lib in libraries:
        subprocess.run([os.path.join(env_name, "Scripts", "pip"), "install", lib], check=True)
    
    #Re-Run the script with the Virtual Env Activated
    python_exe = os.path.join(env_name, "Scripts", "python")
    subprocess.run([python_exe, __file__])



from scipy.optimize import linprog

# Coeficientes de la función objetivo
c = [400, 400, 300, 300, 320, 320]

# Restricciones de igualdad
A_eq = [
    [2, 2, 1, 1, 2, 2],  # 2FDF + 2DFD + FD + DF + 2FDF_S + 2DFD_S = 10
    [1, 1, 0, 0, 1, 1],  # FDF + DFD + FD + FDF_S + DFD_S = 5
    [1, 1, 1, 1, 1, 1],  # FDF + DFD + DF + FDF_S + DFD_S = 5
]

b_eq = [10, 5, 5]

# Restricciones de igualdad para FD y DF
A_eq_2 = [
    [0, 0, 1, -1, 0, 0]  # FD = DF
]

b_eq_2 = [0]

# Restricción para FDF + FD + FDF_S ≥ 1
A_ub = [
    [-1, 0, 0, 0, -1, 0],  # FDF + FD + FDF_S >= 1
]

b_ub = [-1]

# Restricciones de no negatividad
bounds = [(0, None)] * 6  # FDF, DFD, FD, DF, FDF_S, DFD_S >= 0

# Resolver el problema
res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq + A_eq_2, b_eq=b_eq + b_eq_2, bounds=bounds, method='highs')

# Mostrar resultados
if res.success:
    print("Solución encontrada:")
    print("Valores de las variables:", res.x)
    print("Costo total mínimo:", res.fun)
else:
    print("No se encontró solución.")
input("Press any key to Exit")

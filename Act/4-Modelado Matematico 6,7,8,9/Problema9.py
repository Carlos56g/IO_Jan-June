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
    libraries = ["pulp"]
    for lib in libraries:
        subprocess.run([os.path.join(env_name, "Scripts", "pip"), "install", lib], check=True)
    
    #Re-Run the script with the Virtual Env Activated
    python_exe = os.path.join(env_name, "Scripts", "python")
    subprocess.run([python_exe, __file__])


import pulp

# Número de variables (R_1, R_2, ..., R_10)
n = 10

# Crear un problema de minimización
prob = pulp.LpProblem("Minimizar_Recompensas", pulp.LpMinimize)

# Crear variables R_i, que son enteras y mayores que 0
R = [pulp.LpVariable(f"R_{i+1}", lowBound=1, cat='Integer') for i in range(n)]  # Variables enteras y >= 1

# Función objetivo: Minimizar la suma de R_i
prob += pulp.lpSum(R), "Suma_Recompensas"

# Resolver el problema
prob.solve()

# Mostrar los resultados
if pulp.LpStatus[prob.status] == "Optimal":
    print("La solución óptima es:")
    for r in R:
        print(f"{r.name}: {r.varValue}")
    print("Suma total:", pulp.value(prob.objective))
else:
    print("No se pudo encontrar una solución óptima")
input("Press any key to Exit")
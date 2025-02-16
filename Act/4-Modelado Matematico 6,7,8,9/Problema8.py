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


from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Definir el problema de optimización
prob = LpProblem("Minimizar_Cortes_Soldaduras", LpMinimize)

# Definir variables de decisión x_(i,j), donde i es la posición en la cadena y j es la cadena
x = {(i, j): LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for i in range(1, 4) for j in range(1, 5)}

# Función objetivo: minimizar C_B = 5 * sum(x_(i,j) para todas las i y j)
prob += 5 * lpSum(x[i, j] for i in range(1, 4) for j in range(1, 5)), "Costo_Total"

# Restricción: x_3,1 + x_3,2 + x_3,3 + x_3,4 = 4
prob += lpSum(x[3, j] for j in range(1, 5)) == 4, "Restriccion_Cortes_Soldaduras"

# Restricciones adicionales
prob += lpSum(x[i, 1] for i in range(1, 4)) >= 1, "Restriccion_Cadena_1"
prob += lpSum(x[i, 2] for i in range(1, 4)) >= 1, "Restriccion_Cadena_2"
prob += lpSum(x[i, 3] for i in range(1, 4)) >= 1, "Restriccion_Cadena_3"
prob += lpSum(x[i, 4] for i in range(1, 4)) >= 1, "Restriccion_Cadena_4"

# Resolver el problema
prob.solve()

# Mostrar la matriz de resultados
print("Matriz de resultado (x_(i,j)):")
resultado = [[x[i, j].varValue for j in range(1, 5)] for i in range(1, 4)]
for fila in resultado:
    print(fila)

# Interpretación de resultados
print("\nInterpretación de los cortes y soldaduras:")
for i in range(1, 4):
    for j in range(1, 5):
        if x[i, j].varValue > 0:
            siguiente_cadena = (j + 1) if j < 4 else 1
            print(f"Se cortó el eslabón {i} de la cadena {j} y se soldó al eslabón 1 de la cadena {siguiente_cadena}.")
input("Press any key to Exit")
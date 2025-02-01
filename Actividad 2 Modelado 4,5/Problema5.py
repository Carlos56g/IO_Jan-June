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

from scipy.optimize import minimize

# Función de pago para ambos jugadores
def pago(J_C, C_C):
    return 0.3 - 0.2 * C_C - 0.1 * J_C + 0.5 * J_C * C_C

# Función de optimización conjunta (maximizar para J_C, minimizar para C_C)
def optimizacion_conjunta(X):
    J_C, C_C = X
    # Queremos maximizar para J_C, minimizando para C_C
    return -pago(J_C, C_C)  # Negamos para que scipy lo minimice

# Restricciones de las variables
bounds = [(0, 1), (0, 1)]  # 0 <= J_C <= 1, 0 <= C_C <= 1

# Condición inicial para J_C y C_C
J_C_inicial = 0.4 #VALORES OBTENIDOS POR MEDIO DE DERIVACION PARCIAL
C_C_inicial = 0.2

# Resolución del problema usando scipy.optimize.minimize
resultado = minimize(optimizacion_conjunta, [J_C_inicial, C_C_inicial], bounds=bounds)

# Imprimir el resultado
J_C_optimo, C_C_optimo = resultado.x
print(f"El valor óptimo de J_C es: {J_C_optimo}")
print(f"El valor óptimo de C_C es: {C_C_optimo}")
print(f"Con un porcentaje de exito de: {-resultado.fun}")
input("Press any key to Exit")
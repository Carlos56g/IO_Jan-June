#Automatic creation of an virtual environment to run the script and intall the libraries
import subprocess
import os
import venv
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
env_name = os.path.join(script_dir, "VirtualEnv")
if os.path.exists(os.path.join(script_dir, "VirtualEnv")):
    pass
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
#Checks if the VirtualEnv is activated (This is the path to the Python installation currently in use. If the virtual environment is active, sys.prefix will point to the virtual environment directory, while sys.base_prefix points to the global Python installation.)
if sys.prefix == sys.base_prefix:
    print("Activating the Virtual Environment...")
    python_exe = os.path.join(env_name, "Scripts", "python")
    subprocess.run([python_exe, __file__])

from scipy.optimize import minimize_scalar

# Función objetivo: Área negativa (para minimizar)
def area(h):
    w = 50 - h  # Restricción w + h = 50
    return -(h * w)  # Negativo porque queremos maximizar

# Resolver el problema
res = minimize_scalar(area, bounds=(0, 50), method='bounded')

# Mostrar resultados
if res.success:
    h_opt = res.x
    w_opt = 50 - h_opt
    print(f"h (altura): {h_opt:.2f}")
    print(f"w (ancho): {w_opt:.2f}")
    print(f"Área máxima: {-res.fun:.2f}")
else:
    print("No se encontró solución.")
input("Press any key to Exit")

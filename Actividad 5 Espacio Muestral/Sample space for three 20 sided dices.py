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
    libraries = ["tabulate", "matplotlib"]
    for lib in libraries:
        subprocess.run([os.path.join(env_name, "Scripts", "pip"), "install", lib], check=True)
    
    #Re-Run the script with the Virtual Env Activated
    python_exe = os.path.join(env_name, "Scripts", "python")
    subprocess.run([python_exe, __file__])


"""Sample space for the random experiment of rolling three 20-sided dices."""
from tabulate import tabulate
import matplotlib.pyplot as plt
#First list all the possible results for each dices
sides1=[i for i in range(1,21)]
sides2=[i for i in range(1,21)]
sides3=[i for i in range(1,21)]

#Second, create a list of all possible outcomes for the three dices
total_results=[
    [i,j,k]
    for i in sides1
    for j in sides2
    for k in sides3
    ]

#Third, define a Random Variable x that represents the sum of the three dices
x=[sum(i) for i in total_results]

#Fourth, create a dictionary that represents the frequency of each possible sum
x_freq={x[i]:x.count(x[i]) for i in range(len(x))}

#Extra step, to be able to use the tabulate function
x_freq_list=[(key,value) for key,value in x_freq.items()]

#Fifth, create a table with each possible sum and its frequency
print("Table of Frequency of the Random Experiment of rolling three 20-sided dices.")
print(tabulate(x_freq_list, ["Sum","Freq"], tablefmt="github"))

#Sixth, create a graph with the data obtained
x=[key for key,item in x_freq.items()]
y=[item for key,item in x_freq.items()]
plt.plot(x,y)
plt.title("Sample space for the random experiment of rolling three 20-sided dice")
plt.xlabel("Random Value of X")
plt.ylabel("Frequency")
plt.show()

input("Press any key to Exit")
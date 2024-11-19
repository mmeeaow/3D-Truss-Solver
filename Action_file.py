import Inputs as i
import multiprocessing as mp
from tkinter import messagebox
import numpy as np
import scipy as sp
import subprocess

Data = i.select_input_file()

messagebox.showinfo(title="Progress", message= "Starting solving process.")

def post_process():
    subprocess.run(['python', 'Post_processing.py'], check=True)

dim = i.dimension_combo
E_units = i.Youngs_modulus_combo
F_units = i.force_combo

def Unit_Converter(dim, E_units, F_units):
    Conversion_factor = [0, 0, 0]
    #1st column is for dimension units, 2nd column is for Youngs modulus units, 3rd column is for force units

    #dimension units
    if dim == "Meters":
        Conversion_factor[0] = 1
    elif dim == "Millimeters":
        Conversion_factor[0] = 0.001
    elif dim == "Centimeters":
        Conversion_factor[0] = 0.01
    elif dim == "Inches":
        Conversion_factor[0] = 0.0254
    elif dim == "Feet":
        Conversion_factor[0] = 0.3048
    elif dim == "Yards":
        Conversion_factor[0] = 0.9144
    
    #Youngs Moodulus Units
    if E_units == "GPa":
        Conversion_factor[1] = 10^9
    elif E_units == "MPa":
        Conversion_factor[1] = 10^6
    elif E_units == "psi":
        Conversion_factor[1] = 6894.76
    elif E_units == "ksi":
        Conversion_factor[1] = 6894.76*1000
    
    #Force Units
    if F_units == "Newtons":
        Conversion_factor[2] = 1
    elif F_units == "Kilograms-force":
        Conversion_factor[2] = 9.80665
    elif F_units == "Pounds":
        Conversion_factor[2] = 4.44822
    elif F_units == "Pounds-force":
        Conversion_factor[2] = 4.44822
    
    return Conversion_factor

def remove_empty_entries(Data):
    return [t for t in Data if t == "" or t == 'None' or t == 'nan']

maxJoint = int(max(Data.iloc[:, 0]))
maxMember = int(max(Data.iloc[:, 0]))

Membernode = np.column_stack((Data.iloc[:,11], Data.iloc[:, 12])).astype(int)

Nodecoor = np.column_stack((Data.iloc[:, 1], Data.iloc[:, 2], Data.iloc[:, 3]))
Reactioncoor = np.array([Data.iloc[:, 4], Data.iloc[:, 5], Data.iloc[:, 6]]).T

Force = np.array([Data.iloc[:, 7], Data.iloc[:, 8], Data.iloc[:, 9]]).T

E = Data.iloc[:, 13]
A = Data.iloc[:, 14]

Member_L = np.zeros((maxMember, 1))
c = np.zeros((maxMember, 3))
#1st column is cosx, 2nd column is cosy and 3rd is cosz

for j in range(1, maxMember):
    dx = Nodecoor[Membernode[j, 1], 0] - Nodecoor[Membernode[j, 0], 0]
    dy = Nodecoor[Membernode[j, 1], 1] - Nodecoor[Membernode[j, 0], 1]
    dz = Nodecoor[Membernode[j, 1], 2] - Nodecoor[Membernode[j, 0], 2]
    Member_L[j, 0] = np.sqrt(dx**2 + dy**2 + dz**2)
    c[j, 0] = dx / Member_L[j, 0]
    c[j, 1] = dy / Member_L[j, 0]
    c[j, 2] = dz / Member_L[j, 0]

global_K = np.zeros((3*maxJoint, 3*maxJoint))

for j in range(1, maxMember):
    K = E.iloc[j] * A.iloc[j] / Member_L[j, 0]
    
    #The multiple different cos product terms are calculated here
    c2 = np.array((c[j, 0]**2, c[j, 1]**2, c[j, 2]**2))
    cp = np.array((c[j, 0]*c[j, 1], c[j, 0]*c[j, 2], c[j, 1]*c[j, 2]))

    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 2] += K*c2[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 1] += K*cp[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 0] += K*cp[1]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 2] -= K*c2[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 1] -= K*cp[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 0] -= K*cp[1]

#row 2
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 2] += K*cp[0]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 1] += K*c2[1]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 0] += K*cp[2]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 2] -= K*cp[0]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 1] -= K*c2[1]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 0] -= K*cp[2]

#row 3
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 0] - 2] += K*cp[1]
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 0] - 1] += K*cp[2]
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 0] - 0] += K*c2[2]
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 1] - 2] -= K*cp[1]
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 1] - 1] -= K*cp[2]
    global_K[3*Membernode[j, 0] - 0, 3*Membernode[j, 1] - 0] -= K*c2[2]

#row 4
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 2] -= K*c2[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 1] -= K*cp[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 0] -= K*cp[1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 2] += K*c2[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 1] += K*cp[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 0] += K*cp[1]

#row 5
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 2] -= K*cp[0]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 1] -= K*c2[1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 0] -= K*cp[2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 2] += K*cp[0]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 1] += K*c2[1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 0] += K*cp[2]

#row 6
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 0] - 2] -= K*cp[1]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 0] - 1] -= K*cp[2]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 0] - 0] -= K*c2[2]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 2] += K*cp[1]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 1] += K*cp[2]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 0] += K*c2[2]

print(Force)
#load vector
def load_func(Force):
    load = np.zeros((3*maxJoint,1))
    for j in range(maxJoint):
        for k in range(0, 3):
            load[3*j - (2-k)] = Force[j, k]

    return load

global_K_store = global_K
for i in range(maxJoint):
    for j in range(0, 3):
        if Reactioncoor[i, j] == 1:
            global_K_store[:, 3*i - (2-j)] = 0
            global_K_store[3*i - (2-j), :] = 0
            global_K_store[3*i - (2-j), 3*i - (2-j)] = 1



load = load_func(Force)
#Actual Solution process

N_disp = np.linalg.solve(global_K_store, load)

N_result = np.zeros((maxJoint, 3))

for j in range(maxJoint):
    for k in range(3):
        N_result[j, k] = N_disp[3*j - (2-k)]

Stresses = np.zeros((maxMember, 1))
du = [0, 0, 0]

for i in range(maxMember):
    #Directional Displacements
    du[1] = c[j, 0] * (N_result[Membernode[i, 1], 0] - N_result[Membernode[i, 0], 0])
    du[2] = c[j, 1] * (N_result[Membernode[i, 1], 1] - N_result[Membernode[i, 0], 1])
    du[3] = c[j, 2] * (N_result[Membernode[i, 1], 2] - N_result[Membernode[i, 0], 2])

    Stresses[i, 0] = (E[i, 0]/Member_L[i, 0])*(du[0] + du[1] + du[2])

#Reaction forces
R = global_K * N_disp
Reaction3d = np.zeros((maxJoint, 3))

for j in range(maxJoint):
    for k in range(3):
        Reaction3d[j, k] = R[3*j - (2-k)]

post_process()


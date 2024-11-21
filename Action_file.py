import Inputs as i
import multiprocessing as mp
from tkinter import messagebox
import numpy as np
import scipy as sp
import subprocess
import time

[Data, kgorlbs, dim, E_units, F_units, core_usage] = i.search_and_destroy()
def post_process():
    subprocess.run(['python', 'Post_processing.py'], check=True)


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

Conv = Unit_Converter(dim, E_units, F_units)
print(dim, E_units, F_units)

Data = Data.to_numpy().astype(float)


maxJoint = int(max(Data[:, 0]))
maxMember = int(max(Data[:, 10]))


Nodecoor = Data[:, [1,2,3]]#node coordinates
Reactioncoor = Data[:, [4,5,6]]#reaction force directions
Force = Data[:, [7,8,9]]#applied load
Membernode = Data[:, [11, 12]].astype(int) #Member connecting nodes. 1st column is pipe start, 2nd is pipe end
E = Data[:, 13]#Youngs modulus of each pipe
A = Data[:, 14]#Cross Sectional Area

def remove_emptiness(var):
    var = var[~np.isnan(Data).any(axis=1)]
    return var


#removiing all the empty rows from the data
Nodecoor = remove_emptiness(Nodecoor)
Reactioncoor = remove_emptiness(Reactioncoor)
Force = remove_emptiness(Force)


Member_L = np.zeros((maxMember, 1))
c = np.zeros((maxMember, 3))
for j in range(maxMember):
    
    dx = Nodecoor[Membernode[j, 1]-1, 0] - Nodecoor[Membernode[j, 0]-1, 0]
    dy = Nodecoor[Membernode[j, 1]-1, 1] - Nodecoor[Membernode[j, 0]-1, 1]
    dz = Nodecoor[Membernode[j, 1]-1, 2] - Nodecoor[Membernode[j, 0]-1, 2]
    Member_L[j, 0] = np.sqrt(dx**2 + dy**2 + dz**2)
    c[j, 0] = dx / Member_L[j, 0]
    c[j, 1] = dy / Member_L[j, 0]
    c[j, 2] = dz / Member_L[j, 0]

global_K = np.zeros((3*maxJoint, 3*maxJoint))

for j in range(maxMember):

    K = E[j] * A[j] / Member_L[j, 0]

    #The multiple different cos product terms are calculated here
    c2 = np.array((c[j, 0]**2, c[j, 1]**2, c[j, 2]**2))
    cp = np.array((c[j, 0]*c[j, 1], c[j, 0]*c[j, 2], c[j, 1]*c[j, 2]))

    

    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 0] - 3] += K*c2[0]
    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 0] - 2] += K*cp[0]
    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 0] - 1] += K*cp[1]
    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 1] - 3] -= K*c2[0]
    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 1] - 2] -= K*cp[0]
    global_K[3*Membernode[j, 0] - 3, 3*Membernode[j, 1] - 1] -= K*cp[1]

#row 2
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 3] += K*cp[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 2] += K*c2[1]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 0] - 1] += K*cp[2]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 3] -= K*cp[0]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 2] -= K*c2[1]
    global_K[3*Membernode[j, 0] - 2, 3*Membernode[j, 1] - 1] -= K*cp[2]

#row 3
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 3] += K*cp[1]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 2] += K*cp[2]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 0] - 1] += K*c2[2]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 3] -= K*cp[1]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 2] -= K*cp[2]
    global_K[3*Membernode[j, 0] - 1, 3*Membernode[j, 1] - 1] -= K*c2[2]

#row 4
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 0] - 3] -= K*c2[0]
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 0] - 2] -= K*cp[0]
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 0] - 1] -= K*cp[1]
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 1] - 3] += K*c2[0]
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 1] - 2] += K*cp[0]
    global_K[3*Membernode[j, 1] - 3, 3*Membernode[j, 1] - 1] += K*cp[1]

#row 5
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 3] -= K*cp[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 2] -= K*c2[1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 0] - 1] -= K*cp[2]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 3] += K*cp[0]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 2] += K*c2[1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 1] += K*cp[2]

#row 6
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 3] -= K*cp[1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 2] -= K*cp[2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 0] - 1] -= K*c2[2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 3] += K*cp[1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 2] += K*cp[2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 1] += K*c2[2]
global_k_store = global_K.copy()

load = np.zeros((3*maxJoint, 1))

for j in range(maxJoint):
    for k in range(3):
        load[3*j - (2-k)] = Force[j, k]

#the matrix to calculate reaction forces


for i in range(1, maxJoint+1):
    for j in range(1, 4):
         if Reactioncoor[i-1, j-1] == 1:
            
            global_k_store[:, 3*i - (4-j)] = 0
            global_k_store[3*i - (4-j), :] = 0
            global_k_store[3*i - (4-j), 3*i - (4-j)] = 1

# np.savetxt('perf01.csv', global_K, delimiter=',')

N_disp = np.linalg.solve(global_k_store, load)
N_result = np.zeros((maxJoint, 3))

for j in range(1, maxJoint + 1):
    for k in range(1, 4):
        N_result[j-1, k-1] = N_disp[3*j - (4-k)].item()

Stresses = np.zeros((maxMember, 1))
du = [0, 0, 0]

for i in range(maxMember):
    
    #Directional Displacements
    du[0] = c[j, 0] * (N_result[Membernode[i, 1]-1, 0] - N_result[Membernode[i, 0]-1, 0])
    du[1] = c[j, 1] * (N_result[Membernode[i, 1]-1, 1] - N_result[Membernode[i, 0]-1, 1])
    du[2] = c[j, 2] * (N_result[Membernode[i, 1]-1, 2] - N_result[Membernode[i, 0]-1, 2])

    Stresses[i] = (E[i]/Member_L[i])*(du[0] + du[1] + du[2])

#Reaction forces
R = (global_K @ N_disp) - load
Reaction3d = np.zeros((maxJoint, 3))

for j in range(1, maxJoint + 1):
    for k in range(1,4):
        Reaction3d[j-1, k-1] = R[3*j - (4-k)].item()



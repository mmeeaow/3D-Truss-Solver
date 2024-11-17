import Inputs as i
import multiprocessing as mp
from tkinter import messagebox
import numpy as np
import scipy as sp

Data = None

while Data == None:
    Data = i.select_input_file()

messagebox.showinfo("Progress", "File has been selected.")

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

maxJoint = max(Data[:, 1])
maxMember = max(Data[:, 11])

Membernode = [Data[:,12], Data[:, 13]]

Nodecoor = [Data[:, 2], Data[:, 3], Data[:, 4]]
Reactioncoor = [Data[:, 5], Data[:, 6], Data[:, 7]]

E = Data[:, 14]
A = Data[:, 15]

Member_L = np.zeros(maxMember, 1)
c = [maxMember, 3]
#1st column is cosx, 2nd column is cosy and 3rd is cosz

for j in range(1, maxMember):
    dx = Nodecoor[Membernode[j, 2], 1] - Nodecoor[Membernode[j, 1], 1]
    dy = Nodecoor[Membernode[j, 2], 2] - Nodecoor[Membernode[j, 1], 2]
    dz = Nodecoor[Membernode[j, 2], 3] - Nodecoor[Membernode[j, 1], 3]
    Member_L[j, 1] = np.sqrt(dx^2 + dy^2 + dz^2)
    c[j, 1] = dx / Member_L[j, 1]
    c[j, 2] = dy / Member_L[j, 1]
    c[j, 3] = dz / Member_L[j, 1]

global_K = np.zeros[3*maxJoint]

for j in range(1, maxMember):
    K = E[ j, 1] * A[ j, 1] / Member_L[j, 1]
    
    #The multiple different cos product terms are calculated here
    c2 = [c[j, 1]^2, c[j, 2]^2, c[j, 3]^2]
    cp = [c[j, 1]*c[j, 2], c[j, 1]*c[j, 3], c[j, 2]*c[j, 3]]
    
    #row 1
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 2] += K*c2[j, 1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 1] += K*cp[j, 1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 1] - 0] += K*cp[j, 2]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 2] - 2] -= K*c2[j, 1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 2] - 1] -= K*cp[j, 1]
    global_K[3*Membernode[j, 1] - 2, 3*Membernode[j, 2] - 0] -= K*cp[j, 2]

    #row 2
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 2] += K*cp[j, 1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 1] += K*c2[j, 2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 1] - 0] += K*cp[j, 3]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 2] - 2] -= K*cp[j, 1]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 2] - 1] -= K*c2[j, 2]
    global_K[3*Membernode[j, 1] - 1, 3*Membernode[j, 2] - 0] -= K*cp[j, 3]

    #row 3
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 2] += K*cp[j, 2]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 1] += K*cp[j, 3]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 1] - 0] += K*c2[j, 3]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 2] - 2] -= K*cp[j, 2]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 2] - 1] -= K*cp[j, 3]
    global_K[3*Membernode[j, 1] - 0, 3*Membernode[j, 2] - 0] -= K*c2[j, 3]

    #row 4
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 1] - 2] -= K*c2[j, 1]
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 1] - 1] -= K*cp[j, 1]
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 1] - 0] -= K*cp[j, 2]
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 2] - 2] += K*c2[j, 1]
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 2] - 1] += K*cp[j, 1]
    global_K[3*Membernode[j, 2] - 2, 3*Membernode[j, 2] - 0] += K*cp[j, 2]

    #row 5
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 1] - 2] -= K*cp[j, 1]
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 1] - 1] -= K*c2[j, 2]
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 1] - 0] -= K*cp[j, 3]
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 2] - 2] += K*cp[j, 1]
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 2] - 1] += K*c2[j, 2]
    global_K[3*Membernode[j, 2] - 1, 3*Membernode[j, 2] - 0] += K*cp[j, 3]

    #row 6
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 1] - 2] -= K*cp[j, 2]
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 1] - 1] -= K*cp[j, 3]
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 1] - 0] -= K*c2[j, 3]
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 2] - 2] += K*cp[j, 2]
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 2] - 1] += K*cp[j, 3]
    global_K[3*Membernode[j, 2] - 0, 3*Membernode[j, 2] - 0] += K*c2[j, 3]

messagebox.showinfo(f"The K matrix formed is: {global_K}")
   

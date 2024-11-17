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






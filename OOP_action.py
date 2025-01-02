import numpy as np
import pandas as pd
import multiprocessing as mp
import time, os
from tkinter import Tk
import Inputs as i


class data:
    def __init__(self):
        self.file = i.main()
        self.file = self.file.to_numpy().astype(float)
        self.units = pd.read_json('user_inputs.json', orient='records', lines=True)
    


class UnitConv:
    def __init__(self):
        self.unit_system = data().units['unit system']
        self.l = data().units['length unit']
        self.E = data().units['youngs modulus unit']
        self.F = data().units['force unit']

    def l_factor(self):
        if self.unit_system == 'Metric':
            match self.l:
                case 'mm':
                    return 1e-3
                case 'cm':
                    return 1e-2
                case 'm':
                    return 1
        elif self.unit_system == 'Imperial':
            match self.l:
                case 'in':
                    return 1
                case 'ft':
                    return 12
                case 'yd':
                    return 36
    
    def E_factor(self):
        if self.unit_system == 'Metric':
            match self.E:
                case 'Gpa':
                    return 1e9
                case 'MPa':
                    return 1e6
        elif self.unit_system == 'Imperial':
            match self.E:
                case 'psi':
                    return 1
                case 'ksi':
                    return 1000

    def F_factor(self):
        if self.unit_system == 'Metric':
            match self.F:
                case 'N':
                    return 1
                case 'kN':
                    return 1000
                
        elif self.unit_system == 'Imperial':
            match self.F:
                case 'lbf':
                    return 1
                case 'kips':
                    return 1000

class Material:
    def __init__(self, E, A):
        self.E = E * UnitConv().E_factor()
        self.A = A * (UnitConv().l_factor())**2

class Node:
    def __init__(self, x, y, z):
       self.coordinates = np.array([x, y, z])

class Member:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
    


# class Structure:



            


#gnmgn
def main2():
    app = data()
    print(app.file, app.units)


#main2()
        


        
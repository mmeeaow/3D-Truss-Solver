import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from numpy import cos as c
from numpy import radians as rad

def select_coordinate_csv_file():

    #file dialog open to ask for a csv file
    f_p = filedialog.askopenfilename(
        title = "Please select a file with the frame dimensions:",
        filetypes = [("CSV files", "*.csv")]
    )

    #check if a file is selected
    if f_p:
        print(f"File selected: {f_p}")
        try:
            result = np.loadtxt(f_p, delimiter = ",", skiprows = 1, dtype=np.float64)
            return result
        except IOError:
            print(f"The selected file {f_p} was not readable.")
            return None
    return None
    #right now there is no method to ensure that there are exactly 7 columns in the csv file
    #so we just hope that the file has only 7 columns automatically 

def select_load_csv_file():
    f_p = filedialog.askopenfilename(
        title = "Please define a file with Loads at each node:",
        filetypes = [("CSV files", "*.csv")]
    )

    #check if a file is selected
    if f_p:
        print(f"File selected: {f_p}")
        try:
            result = np.loadtxt(f_p, delimiter = ",", skiprows = 1, dtype = float)
            return result
        except IOError:
            print(f"The selected file {f_p} was not readable.")
            return None
    return None
    #right now there is no method to ensure that there are exactly 3 columns in the csv file
    #so we just hope that the file has only 3 columns automatically

def  truss_solver():
    #the start of the real shit
    coor = None
    loads = None
    while coor is None:
        coor =  select_coordinate_csv_file()
    

    while loads is None:
        loads = select_load_csv_file()
                 
    
    print("Both files have been selected.")
    r_coor = int(np.max(coor[:,5]) + 1)
    r_load = loads.shape[0] 

    
   
    g_stiff_matrix = np.zeros((3*r_coor,3*r_coor), dtype=np.float64)
    g_load_matrix = np.zeros((3*r_load, 1), dtype=np.float64)
    g_support_matrix = np.zeros((3*r_load, 1), dtype=np.float64)
    r_matrix = np.zeros((3*r_coor,3*r_coor), dtype=np.float64)

    for row in coor:
        L = row[0]
        roll = rad (row[1])
        pitch = rad (row[2])
        yaw = rad (row[3])
        start = int(row[4])
        end = int(row[5])
        E = row[6]
        dout = row[7]
        t = row[8]
        
        Area = np.pi * 0.25 * 0.000001 * (((dout)**2) - ((dout - 2*t)**2))

        local_k = E * Area / (L*0.001)

        A = np.array( [[c(roll)**2, c(roll)*c(pitch), c(roll)*c(yaw)], 
                     [c(roll)*c(pitch), c(pitch)**2, c(pitch)*c(yaw)],
                     [c(roll)*c(yaw), c(pitch)*c(yaw), c(yaw)**2]])
        A = local_k * A
        #the first matrix
        for i in range(3):
            for j in range(3):
                g_stiff_matrix[3*start + i, 3*start + j] +=  A[i, j]

        #second matrix
        for i in range(3):
            for j in range(3):
                g_stiff_matrix[3*end + i, 3*end + j] +=  A[i, j]
        
        #third matrix
        for i in range(3):
            for j in range(3):
                g_stiff_matrix[3*start + i, 3*end + j] -=  A[i, j]
        
        #fourth matrix
        for i in range(3):
            for j in range(3):
                g_stiff_matrix[3*end + i, 3*start + j] -=  A[i, j]



    for ind in range(loads.shape[0]):
        for i in range(3):            
                g_load_matrix[3*ind + i] += loads[ind,i]
    
    for ind2 in range(loads.shape[0]):
        for k in range(3,6):
            if loads[ind2, k] == 1:
                g_support_matrix[3*ind2 + k - 3] = 1

    for count in range(g_support_matrix.shape[0]):
        if g_support_matrix[count] == 1:
            r_matrix[count, :] = g_stiff_matrix[count, :]
            r_matrix[:, count] = g_stiff_matrix[:, count]
            g_stiff_matrix[count, :] = 0
            g_stiff_matrix[:, count] = 0
            g_stiff_matrix[count, count] = 1
    print(g_support_matrix)
    print(r_matrix)
    print(g_stiff_matrix)
    print(g_load_matrix)

    Sol = np.linalg.solve(g_stiff_matrix, g_load_matrix)

    outfile = 'Solved.csv'
    np.savetxt(outfile, Sol, delimiter=',', header='Column1', comments='', fmt='%d')
    
    print(f"Solution saved with file name {outfile}")

                

root = tk.Tk()
root.title("Truss Calculator")

select_button = tk.Button(root, text="Select CSV Files", command=truss_solver)
select_button.pack(pady=21)


# Start the GUI event loop
root.mainloop()
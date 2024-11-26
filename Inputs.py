#Initial file, to get all the inputs from the user. Might also add some graphic design later.

import tkinter as k
from tkinter import ttk
from tkinter import filedialog, messagebox
from pandas import read_excel
import psutil
import subprocess


def update_units(*args):
    # This function is called whenever the user selects a unit from the dropdown menu.
    unit_system = unit_system_var.get()

    if unit_system == "Metric":
        dimension_units = ["Meters", "Centimeters", "Millimeters"]
        Youngs_modulus_units = ["GPa", "MPa"]
        Force_units = ["Newtons", "Kilograms-force"]

    elif unit_system == "Imperial":
        dimension_units = ["Feet", "Inches", "Yards"]
        Youngs_modulus_units = ["psi", "ksi"]
        Force_units = ["Pounds", "Pounds-force"]

    
    dimension_combo['values'] = dimension_units
    Youngs_modulus_combo['values'] = Youngs_modulus_units
    force_combo['values'] = Force_units

def submit():
    isitin = 0
    while isitin == 0:
        v1 = unit_system_var.get()
        v2 = dimension_combo.get()
        v3 = Youngs_modulus_combo.get()
        v4 = force_combo.get()
        v5 = num_cores_var.get()
        
        dict = {
            'Unit system': v1,
            'Length Unit': v2,
            'Youngs Modulus Unit': v3,
            'Force Unit': v4,
            'Number of Cores': v5
        }
        for nem, vel in dict.items():
            if vel == None:
                messagebox.showerror("Error", f"No value selected for {nem}. Please resubmit values")
                v1 = unit_system_var.get()
                v2 = dimension_combo.get()
                v3 = Youngs_modulus_combo.get()
                v4 = force_combo.get()
                v5 = num_cores_var.get()
                
        v0 = select_input_file()
            
        if vel != None:
            isitin = 1

    root.destroy()


    return v0, v1, v2, v3, v4, v5

def select_input_file():


    user_file = filedialog.askopenfilename(
        title="Select Input File",
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if user_file:
        messagebox.showinfo(message= f"File Selected: {user_file}")
        try:
            inputs = read_excel(user_file, skiprows = 0, dtype = float)
            if inputs.shape[1] != 15:
               messagebox.showerror("Error", "The selected file was not readable. Please ensure it has the correct number of columns.")
               return None
            else:
                return inputs
        except Exception as e:
            messagebox.showerror("Error", "Error: The file selected is not a valid XLSX file.\n" + str(e))
            return None
    return None

#def complete_calculation():
    #subprocess.run(['python', 'Action_file.py'], check = False)





#main window
root = k.Tk()
root.title("Truss Solver")

#drop down menu for unit system
unit_system_var = k.StringVar(value = "Metric")

unit_system_label = k.Label(root, text="Select Unit System:")
unit_system_label.pack()
unit_system_combo = ttk.Combobox(root, textvariable=unit_system_var)
unit_system_combo['values'] = ("Metric", "Imperial")
unit_system_combo.pack()

#update the units based on the selected unit system
unit_system_var.trace_add("write", update_units)

#drop down menu for the dimension units
dimension_label = k.Label(root, text="Select Dimension Unit:")
dimension_label.pack()
dimension_combo = ttk.Combobox(root)
dimension_combo.pack()

# Drop-down for Young's modulus units
youngs_modulus_label = k.Label(root, text="Select Young's Modulus Unit:")
youngs_modulus_label.pack()
Youngs_modulus_combo = ttk.Combobox(root)
Youngs_modulus_combo.pack()

#Drop down for force units
force_label = k.Label(root, text="Select Force Unit:")
force_label.pack()
force_combo = ttk.Combobox(root)
force_combo.pack()

available_cpu_cores = psutil.cpu_count(logical = False)
num_cores_var = k.StringVar(value="1")
core_label = k.Label(root, text="Select Number of CPU Cores:")
core_label.pack()
num_cores_combo = ttk.Combobox(root, textvariable = num_cores_var)
num_cores_combo['values'] = [str(i) for i in range(1, available_cpu_cores + 1)]
num_cores_combo.pack()

update_units()


select_button1 = k.Button(root, text="Select", command=root.destroy)
select_button1.pack(padx=10, pady=21)

# root.mainloop()
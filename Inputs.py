#Initial file, to get all the inputs from the user. Might also add some graphic design later.

import tkinter as k
from tkinter import ttk
from tkinter import filedialog
from os import cpu_count


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
    kgorlbs = unit_system_var.get()
    dimension = dimension_combo.get()
    Youngs_mod_unit = Youngs_modulus_combo.get()
    force_unit = force_combo.get()
    core_usage = num_core_var.get()


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
unit_system_var.trace_add("w", update_units)

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

available_cpu_cores = cpu_count()
num_core_var = k.StringVar(value="1")
# Drop-down for number of CPU cores
num_cores_label = k.Label(root, text="Select Number of CPU Cores:")
num_cores_label.pack()
num_cores_combo = ttk.Combobox(root, textvariable=num_core_var)
num_cores_combo['values'] = [str(i) for i in range(1, available_cpu_cores - 1)]  # Options from 1 to available cores
num_cores_combo.pack()

update_units()

submit_button = k.Button(root, text="submit", command=submit)
submit_button.pack()



root.mainloop()









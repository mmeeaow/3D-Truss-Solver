from tkinter import ttk, filedialog, messagebox, StringVar, Label, Button, Tk
import pandas as pd
import psutil



class TrussSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Truss Solver")

        # Initialize variables
        self.collected_values = [None] * 5
        self.unit_system_var = StringVar(value="Metric")
        self.num_cores_var = StringVar(value="1")

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        # Dropdown for unit system
        unit_system_label = Label(self.root, text="Select Unit System:")
        unit_system_label.pack()
        self.unit_system_combo = ttk.Combobox(self.root, textvariable=self.unit_system_var)
        self.unit_system_combo['values'] = ("Metric", "Imperial")
        self.unit_system_combo.pack()
        self.unit_system_var.trace_add("write", self.update_units)

        # Dropdown for dimension units
        dimension_label = Label(self.root, text="Select Dimension Unit:")
        dimension_label.pack()
        self.dimension_combo = ttk.Combobox(self.root)
        self.dimension_combo.pack()

        # Dropdown for Young's modulus units
        youngs_modulus_label = Label(self.root, text="Select Young's Modulus Unit:")
        youngs_modulus_label.pack()
        self.Youngs_modulus_combo = ttk.Combobox(self.root)
        self.Youngs_modulus_combo.pack()

        # Dropdown for force units
        force_label = Label(self.root, text="Select Force Unit:")
        force_label.pack()
        self.force_combo = ttk.Combobox(self.root)
        self.force_combo.pack()

        # Dropdown for CPU cores
        available_cpu_cores = psutil.cpu_count(logical=False)
        core_label = Label(self.root, text="Select Number of CPU Cores:")
        core_label.pack()
        self.num_cores_combo = ttk.Combobox(self.root, textvariable=self.num_cores_var)
        self.num_cores_combo['values'] = [str(i) for i in range(1, available_cpu_cores + 1)]
        self.num_cores_combo.pack()

        # Initial call to populate units
        self.update_units()

        # Submit button
        select_button1 = Button(self.root, text="Submit", command=self.handle_submit)
        select_button1.pack(padx=10, pady=21)

    def update_units(self, *args):
        unit_system = self.unit_system_combo.get()
        if unit_system == "Metric":
            dimension_units = ["Meters", "Centimeters", "Millimeters"]
            Youngs_modulus_units = ["GPa", "MPa"]
            Force_units = ["Newtons", "Kilograms-force"]
        elif unit_system == "Imperial":
            dimension_units = ["Feet", "Inches", "Yards"]
            Youngs_modulus_units = ["psi", "ksi"]
            Force_units = ["Pounds", "Pounds-force"]

        self.dimension_combo['values'] = dimension_units
        self.Youngs_modulus_combo['values'] = Youngs_modulus_units
        self.force_combo['values'] = Force_units

    def handle_submit(self):
        # Collect values from ComboBoxes
        self.collected_values[0] = self.unit_system_var.get()
        self.collected_values[1] = self.dimension_combo.get()
        self.collected_values[2] = self.Youngs_modulus_combo.get()
        self.collected_values[3] = self.force_combo.get()
        self.collected_values[4] = int(self.num_cores_combo.get())

        # Close the main window
        self.root.destroy()
    def save_data(self):
        # Save collected values to a JSON file
        data = {
            "unit_system": self.collected_values[0],
            "dimension_unit": self.collected_values[1],
            "Youngs_modulus_unit": self.collected_values[2],
            "force_unit": self.collected_values[3],
            "num_cores": self.collected_values[4]
        }
        data = pd.DataFrame(data)
        data.to_json('data.json', orient='records', lines=True)


# Main execution
if __name__ == "__main__":
    root = Tk()
    app = TrussSolverApp(root)  # Create an instance of the application
    root.mainloop()

    # After the main loop, you can access the collected values
    print("Collected values:", app.collected_values)


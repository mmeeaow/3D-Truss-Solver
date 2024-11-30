from tkinter import ttk, filedialog, messagebox, StringVar, Label, Button, Tk
import pandas as pd
import psutil

class Inputs:
    def __init__(self, root):
        self.root = root
        self.root.title("Inputs")

        self.units = [None] * 5
        self.system = StringVar(value="Metric")
        self.c_count = StringVar(value="1")
        self.file = pd.DataFrame()
        self.ui()

    def ui(self):
        
        #unit system selection
        u_s_label = Label(self.root, text="Select Unit System:")
        u_s_label.pack()
        self.u_s_cb = ttk.Combobox(self.root, textvariable=self.system)
        self.u_s_cb['values'] = ('Metric', 'Imperial')
        self.u_s_cb.pack()
        self.system.trace_add("write", self.unit_change)

        #length unit selection
        l_label = Label(self.root, text="Select Length unit:")
        l_label.pack()
        self.l_cb = ttk.Combobox(self.root)
        self.l_cb.pack()

        #Youngs modulus units
        e_label = Label(self.root, text="Select Youngs Modulus Uniits:")
        e_label.pack()
        self.e_cb = ttk.Combobox(self.root)
        self.e_cb.pack()

        #force units
        f_label = Label(self.root, text="Select Force unit:")
        f_label.pack()
        self.f_cb = ttk.Combobox(self.root)
        self.f_cb.pack()

        #parallelization option
        c_label = Label(text="Select no of cpu cores:")
        c_label.pack()
        c_able = psutil.cpu_count(logical=False)
        self.c_cb = ttk.Combobox(self.root, textvariable=self.c_count)
        self.c_cb['values'] = [str(i) for i in range(1, c_able + 1)]
        self.c_cb.pack()

        self.unit_change()

        

        button1 = Button(self.root, text="Submit", command=self.unit_submit)
        button1.pack(ipadx=10, ipady= 21, padx=10, pady=20)
    def unit_change(self, *args):
        u_s = self.u_s_cb.get()
        if u_s == "Metric":
            self.l_cb['values'] = ('mm', 'cm', 'm')
            self.e_cb['values'] = ('Pa', 'GPa')
            self.f_cb['values'] = ('N', 'kN')
        elif u_s == "Imperial":
            self.l_cb['values'] = ('in', 'ft', 'm')
            self.e_cb['values'] = ('psi', 'ksi')
            self.f_cb['values'] = ('lbf', 'kips')
        
    def file_select(self):
        file = filedialog.askopenfilename(
            title = "Select an input excel file",
            filetypes = [("Excel files", "*.xlsx"), ("Excel files", "*.xls")]    
        )

        if file:
            messagebox.showinfo(f"File Selected {file}")
            try:
                self.file = pd.read_excel(file, skiprows = 0, dtype=float)
                if self.file.shape[1] != 15:
                    messagebox.showerror("Error", "File must have 15 columns")
                    self.file = None
            except Exception as e:
                messagebox.showerror("Error", "Invalid file\n")

    def unit_submit(self):
        #collect data
        self.units[0] = self.system.get()
        self.units[1] = self.l_cb.get()
        self.units[2] = self.e_cb.get()
        self.units[3] = self.f_cb.get()
        self.units[4] = self.c_cb.get()

        self.root.destroy()
        self.file_select()
        data = {
            "unit system" : self.units[0],
            "length unit" : self.units[1],
            "youngs modulus unit" : self.units[2],
            "force unit" : self.units[3],
            "core usage" : self.units[4]            
        }

        data = pd.DataFrame([data])
        data.to_json('user_inputs.json', orient='records', lines=True)
def main():
    if __name__ == "__main__":
        root = Tk()
        app = Inputs(root)
        root.mainloop()


# main()                




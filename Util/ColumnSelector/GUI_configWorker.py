import tkinter as tk
import json

class OptionsTables:

    def __init__(self, window, console):
        self.window = window
        self.console = console
        self.load_config()

    def load_config(self):
        with open('config.json') as f:
            self.config = json.load(f)

        self.cl_SKU_Column = tk.IntVar(value=int(self.config["CL_SKU-Column"]))
        self.pd_SKU_Column = tk.IntVar(value=int(self.config["PD_SKU-Column"]))
        self.cl_Name_Column = tk.IntVar(value=int(self.config["CL_Name-Column"]))
        self.pd_Name_Column = tk.IntVar(value=int(self.config["PD_Name-Column"]))
        self.cl_Num_Table = tk.IntVar(value=int(self.config["CL_Num-Table"]))
        self.pd_Num_Table = tk.IntVar(value=int(self.config["PD_Num-Table"]))
        self.headerFix = tk.BooleanVar(value=bool(self.config["SkipRowLabel"]))

    def save_config(self):
        self.config["CL_SKU-Column"] = self.cl_SKU_Column.get()
        self.config["PD_SKU-Column"] = self.pd_SKU_Column.get()
        self.config["CL_Name-Column"] = self.cl_Name_Column.get()
        self.config["PD_Name-Column"] = self.pd_Name_Column.get()
        self.config["CL_Num-Table"] = self.cl_Num_Table.get()
        self.config["PD_Num-Table"] = self.pd_Num_Table.get()
        self.config["SkipRowLabel"] = self.headerFix.get()

        with open('config.json', 'w') as json_file:
            json.dump(self.config, json_file, indent=4)
        self.console.consoleSend("green", f"Configuration saved.")

    def configure_table(self):
        menu = tk.Toplevel(self.window)
        menu.geometry("450x400")

        # PD Section
        label_pm_sku = tk.Label(menu, text="(Todos los numeros comienzan en zero*)")
        label_pm_sku.grid(row=0, column=2)
        label_pd_sku = tk.Label(menu, text="Base Principal", font=("Helvetica", 12, "bold"))
        label_pd_sku.grid(row=1, column=2, pady=10, sticky='w')

        label_pd_sku = tk.Label(menu, text="Columna a Llenar:")
        label_pd_sku.grid(row=2, column=1, sticky='w')
        entry_pd_sku = tk.Entry(menu, textvariable=self.pd_SKU_Column)
        entry_pd_sku.grid(row=2, column=2)

        label_pd_name = tk.Label(menu, text="Columna Referencia:")
        label_pd_name.grid(row=3, column=1, sticky='w')
        entry_pd_name = tk.Entry(menu, textvariable=self.pd_Name_Column)
        entry_pd_name.grid(row=3, column=2)

        label_pd_num = tk.Label(menu, text="Numero de la tabla:")
        label_pd_num.grid(row=4, column=1, sticky='w')
        entry_pd_num = tk.Entry(menu, textvariable=self.pd_Num_Table)
        entry_pd_num.grid(row=4, column=2)

        # Separator
        separator1 = tk.Label(menu, text="-------------------------------------")
        separator1.grid(row=5, column=2, pady=10, sticky='w')

        # CL Section
        label_cl_sku = tk.Label(menu, text="Base a Importar", font=("Helvetica", 12, "bold"))
        label_cl_sku.grid(row=6, column=2, pady=10, sticky='w')

        label_cl_sku = tk.Label(menu, text="Columna a extraer:")
        label_cl_sku.grid(row=7, column=1, sticky='w')
        entry_cl_sku = tk.Entry(menu, textvariable=self.cl_SKU_Column)
        entry_cl_sku.grid(row=7, column=2)

        label_cl_name = tk.Label(menu, text="Columna de referencia:")
        label_cl_name.grid(row=8, column=1, sticky='w')
        entry_cl_name = tk.Entry(menu, textvariable=self.cl_Name_Column)
        entry_cl_name.grid(row=8, column=2)

        label_cl_num = tk.Label(menu, text="Numero de la tabla:")
        label_cl_num.grid(row=9, column=1, sticky='w')
        entry_cl_num = tk.Entry(menu, textvariable=self.cl_Num_Table)
        entry_cl_num.grid(row=9, column=2)

        headerFix_Check = tk.Checkbutton(menu, text="Marcar solo si hay texto\nen la primera linea", variable=self.headerFix)
        headerFix_Check.grid(row=10, column=1)
        
        # Separator
        separator2 = tk.Label(menu, text="-------------------------------------")
        separator2.grid(row=11, column=2, pady=10, sticky='w')

        save_button = tk.Button(menu, text="Save", command=self.save_config)
        save_button.grid(row=12, column=2, pady=10)

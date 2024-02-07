import tkinter as tk
import json
from plyer import notification
import Util.GUI_Viewer as consoleHandler

f = open('config.json')
data = json.load(f)
def on_entry_click(event):
    if name_var.get() == default_text:
        name_var.set('')
        name_entry.config(fg="black")  # Change text color to black

def NotifDemo():
    notification.notify(
    title='Ejemplo',
    message='Ejemplo.',
    timeout=10  # Notification will be visible for 10 seconds
    )

def submit_name():
    entered_name = name_var.get()
    if len(entered_name) <= 25:
        result_label.config(text=f"Entered Name: {entered_name}", fg="green")
        data["OutputName"] = entered_name
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    else:
        result_label.config(text="Name should be 25 characters long", fg="red")

def on_checkbox_toggle():
    if checkbox_var_Notifs.get():
        data["Notifications"] = bool(checkbox_var_Notifs.get())
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    else:
        data["Notifications"] = bool(checkbox_var_Notifs.get())
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

def on_checkbox_toggle_fix():
    if checkbox_var_Fix.get():
        data["fixIssuesNumbers"] = bool(checkbox_var_Fix.get())
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    else:
        data["fixIssuesNumbers"] = bool(checkbox_var_Fix.get())
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

class Options:

    def __init__(self, window, console):
        self.data = data
        self.window = window
        self.name_var = tk.StringVar()
        self.name_var.set(str(self.data["OutputName"]))
        self.checkbox_var_Notifs = tk.BooleanVar()
        self.name_var.set(bool(self.data["Notifications"]))
        self.checkbox_var_Fix = tk.BooleanVar()
        self.checkbox_var_Fix.set(bool(self.data["fixIssuesNumbers"]))
        self.console = console

    def configure(self):
        menu = tk.Toplevel(self.window)
        menu.geometry("350x300")

        labelName = tk.Label(menu, text="Nombre de archivo de salida: \n(max 25 caracteres)")
        labelName.grid(row=2, column=2)

        labelDate = tk.Label(menu, text=f"+ Fecha actual.csv")
        labelDate.grid(row=3, column=3)
        
        global default_text, name_var, name_entry, result_label, checkbox_var_Notifs, checkbox_var_Fix  # Making these variables global

        default_text = self.data["OutputName"]
        name_var = self.name_var

        name_entry = tk.Entry(menu, width=30, textvariable=name_var, fg="grey")
        name_entry.bind("<FocusIn>", on_entry_click)  # Bind to FocusIn event
        name_entry.grid(row=3, column=2)

        # Create a label to display the result
        result_label = tk.Label(menu, text="")
        result_label.grid(row=4, column=3)

        buttonOUTPUT = tk.Button(menu, text="Guardar", command=submit_name)
        buttonOUTPUT.grid(row=4, column=2)
        
        SeparatorLabel = tk.Label(menu, text="-------------------------------------")
        SeparatorLabel.grid(row=6, column=2)
        
        checkbox_var_Notifs = self.checkbox_var_Notifs
        
        checkboxNTF = tk.Checkbutton(menu, text="Notificaciones", variable=checkbox_var_Notifs, command=on_checkbox_toggle)
        checkboxNTF.grid(row=7, column=2)
        
        buttonTEST = tk.Button(menu, text="Ejemplo", command=NotifDemo)
        buttonTEST.grid(row=7, column=3)
        
        SeparatorLabel = tk.Label(menu, text="-------------------------------------")
        SeparatorLabel.grid(row=8, column=2)
        
        console_instance = self.console
        buttonCONSOLE = tk.Button(menu, text="Mostrar Consola", command=console_instance.consoleShow)
        buttonCONSOLE.grid(row=9, column=2)
        
        SeparatorLabel = tk.Label(menu, text="-------------------------------------")
        SeparatorLabel.grid(row=10, column=2)
        
        checkbox_var_Fix = self.checkbox_var_Fix
        
        InfoLabel = tk.Label(menu, text="Solo activar si tienes problemas con\nnumeros terminando en .0")
        InfoLabel.grid(row=11, column=2)
        checkboxFIX = tk.Checkbutton(menu, text="NumFix", variable=checkbox_var_Fix, command=on_checkbox_toggle_fix)
        checkboxFIX.grid(row=12, column=2)
import tkinter as tk
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from Util.GUI_options import Options
from Util.ColumnSelector.GUI_configWorker import OptionsTables as OptionsTable
from Util.GUI_Viewer import Console as console
from client.DB_Manage import DatabaseConnectionTool as dct
import os

dirCurrent = os.path.dirname(os.path.abspath(__file__))
BaseCL = ""
BasePROD= ""


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"The file '{file_path}' has been deleted.")
    except OSError as e:
        print(f"Error deleting the file '{file_path}': {e}")

def shorten_filename(file_path, max_length=7):
    # Split the file path into the directory, base name, and extension
    directory, file_name = os.path.split(file_path)
    base_name, file_extension = os.path.splitext(file_name)

    # Shorten the base name to the specified length
    shortened_name = base_name[:max_length]

    # Construct the new file name with the original extension
    new_file_name = shortened_name + "... " + file_extension

    # Join the directory and new file name to get the shortened file path
    shortened_file_path = os.path.join(directory, new_file_name)

    return shortened_file_path

def open_new_window():
    # Function to open a new window
    new_window = tk.Toplevel(window)
    new_window.title("Reader | Info")
    new_window.geometry("250x350")
    # Add content to the new window
    new_label = tk.Label(new_window, text="This is a new window!")
    new_label.pack(pady=20)

def open_file_PROD():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivos Excel (Produccion)",
        filetypes=[("Archivos Excel", "*.xlsx")]
    )
    if file_path:
        # Check if the selected file has a valid extension
        if file_path.lower().endswith(('.xlsx')):
            print("Selected file: ", file_path)
            dct(window, console_instance).UpdateProd(file_path)
            incorrect_label_PROD.config(text=f"Seleccionado: {shorten_filename(os.path.basename(file_path))}", fg="green")
        else:
            incorrect_label_PROD.config(text="Error! El archivo no es Excel")

def open_file_Cliente():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivos Excel (Cliente)",
        filetypes=[("Archivos Excel", "*.xlsx")]
    )
    if file_path:
        # Check if the selected file has a valid extension
        if file_path.lower().endswith(('.xlsx')):
            print("Selected file:", file_path)
            dct(window, console_instance).UpdateClient(file_path)
            incorrect_label_CL.config(text=f"Seleccionado: {shorten_filename(os.path.basename(file_path))}", fg="green")
        else:
            incorrect_label_CL.config(text="Error! El archivo no es Excel")

def create_separator_top():
    separator_top = tk.Label(window, text="------------- IMPORTAR BASES -------------", font=("Helvetica", 12, "bold"))
    separator_top.grid(row=1, column=1, columnspan=15, pady=10, sticky="nsew")

def create_separator_bottom():
    separator_bottom = tk.Label(window, text="------------------- ACCIONES -------------------", font=("Helvetica", 12, "bold"))
    separator_bottom.grid(row=7, column=2, columnspan=15, pady=10, sticky="nsew")

def deleteFiles():
    delete_file(os.path.join(dirCurrent, "cache", "cachePROD.csv"))
    delete_file(os.path.join(dirCurrent, "cache", "cacheCLIENT.csv"))
# Create the main window
window = tk.Tk()
window.title("Programa | Medalplay")
window.geometry("400x400")

# Load an image
image_path = os.path.join(dirCurrent, "cdn", "info.png")# Replace with the actual path to your image

# Read the Image
opened = Image.open(image_path)

resized = opened.resize((15, 15), resample=Image.LANCZOS)
img = ImageTk.PhotoImage(resized)

# Create a button with an image
button = tk.Button(window, image=img, command=open_new_window, width=20, height=20)
button.grid(row = 0, column = 0)


# FILE SECTION
buttonPROD = tk.Button(window, text="Abrir base PROD", command=open_file_PROD)
buttonPROD.grid(row = 2, column = 2)

# FILE INCORRECT SECTION

incorrect_label_PROD = tk.Label(window, text="", fg="red")
incorrect_label_PROD.grid(row = 2, column = 3)

# FILE SECTION
buttonCLIENT = tk.Button(window, text="Abrir base CLIENTE", command=open_file_Cliente)
buttonCLIENT.grid(row = 3, column = 2)

# FILE INCORRECT SECTION

incorrect_label_CL = tk.Label(window, text="", fg="red")
incorrect_label_CL.grid(row = 3, column = 3)

# SEPARATORS
# Create separators at the top and bottom
create_separator_top()
create_separator_bottom()

console_instance = console(window)
console_instance.consoleShow()
console_instance.lowerConsole()

buttonSTART = tk.Button(window, text="INICIAR\nPROCESO", command=dct(window, console_instance).test, height=8)
buttonSTART.grid(row = 8, column = 2)
buttonSTOP = tk.Button(window, text="CONFIGURAR", command=OptionsTable(window, console_instance).configure_table, height=8)
buttonSTOP.grid(row = 8, column = 3, padx=15)
buttonOPTIONS = tk.Button(window, text="OPCIONES", command=Options(window, console_instance).configure, height=8)
buttonOPTIONS.grid(row = 8, column = 15)

image_path = os.path.join(dirCurrent, "cdn", "logo.png")
lgo = Image.open(image_path)
lgo = ImageTk.PhotoImage(lgo)
window.iconphoto(False, lgo)
window.configure(background='#dcdedc')


deleteFiles()
# Run the Tkinter event loop
window.mainloop()
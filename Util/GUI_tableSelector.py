from tkinter import *


class tooltipSelector:
    def __init__(self, window):
        self.window = window

    def ok(self, variable, master):
        selected_value = variable.get()
        master.destroy()
        return selected_value

    def gui_select(self, options):
        master = Toplevel(self.window)
        master.geometry("200x200")

        variable = StringVar(master)
        variable.set(options[0])  # default value

        w = OptionMenu(master, variable, *options)
        w.pack()

        button = Button(master, text="OK", command=lambda: self.ok(variable, master))
        button.pack()

        # Wait for the window to be destroyed before returning
        master.wait_window()
        return self.ok(variable, master)

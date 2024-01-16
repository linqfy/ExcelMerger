import tkinter as tk
from datetime import datetime

def create_text_widget(parent, text, text_color, font_family="Consolas", font_size=10, font_style="normal"):
    """
    Parameters:
    - parent: The parent widget or window.
    - text: The text to display.
    - font_style: The font style, e.g., "normal", "bold", "italic" (default is "normal").
    """
    custom_font = (font_family, font_size, font_style)
    text_widget = tk.Label(parent, text=text, font=custom_font, fg=text_color,bg="black")
    return text_widget

class Console:
    def __init__(self, window):
        self.window = window
        self.fontCMD = ("Consolas", 10)
        self.console_window = None  # Correctly initializing the attribute
        self.text_widget = None  # Initialize text_widget as None

    def create_text_widget(self):
        # Create a text widget and configure it as needed
        self.text_widget = tk.Text(self.console_window, wrap=tk.WORD, bg="black", fg="green", font=self.fontCMD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.console_window, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=scrollbar.set)

    def consoleShow(self):
        self.console_window = tk.Toplevel(self.window)
        self.console_window.geometry("400x500")
        self.console_window.configure(background='black')
        self.console_window.title("Writer Debug | Console | MedalPlay")

        self.create_text_widget()  # Initialize text_widget

        textConsola = tk.Label(self.console_window, text="Consola | Logs", fg="white", bg="black", font=('Arial', 12, "bold"))
        textConsola.pack()

        hide_button = tk.Button(self.console_window, text="Esconder consola", command=self.hideConsole)
        hide_button.pack(pady=5)

        initial_message = "{} | Consola Iniciada!".format(datetime.now().strftime("%H:%M"))
        self.text_widget.insert(tk.END, initial_message + "\n")


    def consoleSend(self, color, text):
        timestamp = (datetime.now()).strftime("%H:%M")
        message = f"{timestamp} | {text}\n"
        # Create a tag with the specified color
        tag_name = color.lower()  # Convert color name to lowercase
        self.text_widget.tag_configure(tag_name, foreground=color)

        # Apply the tag to the inserted text
        self.text_widget.insert(tk.END, message, tag_name)

        self.text_widget.see(tk.END)  # Scroll to the end


    def hideConsole(self):
        if self.console_window:
            self.console_window.withdraw()  # Use withdraw() to hide the window
    def lowerConsole(self):
        if self.console_window:
            self.console_window.iconify() 
    def showConsole(self):
        if self.console_window:
            self.console_window.deiconify()  # Use deiconify() to show the window

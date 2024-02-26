from client.DB_Open import Reader as rd
from client.DB_Worker import MDOos as worker
import json
import pandas as pd
import random
from Util.NTF_Manage import GlobalNotificationHandler as Notifications
import csv
import tkinter as tk

f = open("config.json")
config = json.load(f)


class DatabaseConnectionTool:

    def __init__(self, window, console, dirWorking):
        self.window = window
        self.notifications = config["Notifications"]
        self.console = console
        self.fileProd = False
        self.dirCurrent = dirWorking

    def test(self):
        if worker(self.console).startWorker():
            Notifications.push("Estado", "El archivo ha sido generado!")

    def UpdateProd(self, fileProd):
        self.fileProd = rd(self.window, self.console).ReadStartProd(fileProd)[0]
        if self.fileProd is not None:
            # Iterate through each cell in the DataFrame
            for col in self.fileProd.columns:
                for idx in self.fileProd.index:
                    cell_value = self.fileProd.at[idx, col]
                    # Check if the cell value ends with ".0"
                    if isinstance(cell_value, float) and cell_value.is_integer():
                        # Remove the ".0" suffix
                        self.fileProd.at[idx, col] = int(cell_value)
            # Write the DataFrame to a CSV file
            self.fileProd.to_csv("cache/cachePROD.csv", index=False)

    def UpdateClient(self, fileClient):
        self.headerFix = bool(config["SkipRowLabel"])  # ROW 0 
        dataRAW = rd(self.window, self.console).ReadStartClient(fileClient)
        self.fileClient = dataRAW[0]
        nameFILE = dataRAW[1]
        if self.fileClient is not None:
            # Write the DataFrame to a CSV file

            statusLabel = tk.Label(
                self.window,
                text=f"La base cliente esta\nusando la tabla:\n{nameFILE}",
                fg="green",
            )
            statusLabel.grid(row=10, column=3)

            self.fileClient.to_csv("cache/cacheCLIENT.csv", index=False)
            if self.headerFix:
                with open("cache/cacheCLIENT.csv", "r", newline="") as infile:
                    reader = csv.reader(infile)
                    next(reader)  # Skip the first line
                    data = list(reader)

                with open("cache/cacheCLIENT.csv", "w", newline="") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(data)

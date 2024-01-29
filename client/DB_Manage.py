from client.DB_Open import Reader as rd
from client.DB_Worker import MDOos as worker
import json
import pandas as pd
import random
from Util.NTF_Manage import GlobalNotificationHandler as Notifications
import os

f = open('config.json')
config = json.load(f)
class DatabaseConnectionTool():
    
    def __init__(self, window, console, dirWorking):
        self.window = window
        self.notifications = config["Notifications"]
        self.console = console
        self.fileProd = False
        self.dirCurrent = dirWorking
    
    def test(self):
        if worker(self.console).startWorker():
            Notifications.push('Estado', "El archivo ha sido generado!")
    
    def UpdateProd(self, fileProd):
        self.fileProd = rd(self.window, self.console).ReadStartProd(fileProd)
        if self.fileProd is not None:
            # Write the DataFrame to a CSV file
            self.fileProd.to_csv(os.path.join(self.dirCurrent, "cache", "cachePROD.csv"), index=False)

    def UpdateClient(self, fileClient):
        self.fileClient = rd(self.window, self.console).ReadStartClient(fileClient)
        if self.fileClient is not None:
            # Write the DataFrame to a CSV file
            self.fileClient.to_csv(os.path.join(self.dirCurrent, "cache", "cacheCLIENT.csv"), index=False)
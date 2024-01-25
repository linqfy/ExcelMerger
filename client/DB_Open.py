import pandas as pd
import chardet
from Util.NTF_Manage import GlobalNotificationHandler as Notifications
import json

f = open('config.json')
data = json.load(f)

class Reader:
    def __init__(self, window, console):
        self.window = window
        self.console_instance = console
        self.config = data
        self.cl_Num_Table = int(self.config["CL_Num-Table"])
        self.pd_Num_Table = int(self.config["PD_Num-Table"])
    
    def detect_encoding(self, file_path):
        self.encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1', 'cp1252', None]  # Add more as needed
        for encoding in self.encodings_to_try:
            self.console_instance.consoleSend("#DFFF00", f"testing: {encoding}")
            try:
                with open(file_path, 'rb') as f:
                    result = chardet.detect(f.read())
                    if result['encoding'] == encoding:
                        self.console_instance.consoleSend("#DFFF00", f"matching encoding found ({encoding})")
                        return encoding
            except Exception as e:
                print(f"Error detecting encoding with {encoding}: {e}")
                self.console_instance.consoleSend("crimson", f"Error detecting encoding with {encoding}: {e}")
                Notifications.push('Estado', "Error al abrir el archivo")

    def read_file(self, file_path, type):
        #try:
            #pass
            #encoding = self.detect_encoding(file_path)
            #df = pd.read_csv(file_path, encoding=encoding)
            #return df
        #except pd.errors.ParserError as e:
            try:
                # self.console_instance.consoleSend("#DFFF00", f"Encoding service worker online!")
                # encoding = self.detect_encoding(file_path)
                
                dm = pd.ExcelFile(file_path)
                
                if type == "prod":
                    print("Reading prod db..")
                    self.console_instance.consoleSend("yellow", f"Reading prod db.. ({file_path}, on table: {self.pd_Num_Table})")
                    
                    df = pd.read_excel(dm, sheet_name=self.pd_Num_Table)#, encoding=encoding)
                else:
                    print("Reading client db..")
                    self.console_instance.consoleSend("yellow", f"Reading client db.. ({file_path}, on table: {self.cl_Num_Table})")
                    
                    df = pd.read_excel(dm, sheet_name=self.cl_Num_Table)#, encoding=encoding)
                
                # Get the list of sheet names
                dfs = dm.sheet_names

                # Check if there are multiple sheets
                if len(dfs) > 1:
                    print(f"The Excel file has multiple sheets: {dfs}")
                    self.console_instance.consoleSend("yellow", f"WARNING: Table has multiple sheets {dfs}, selecting default on config.json")
                else:
                    print("The Excel file has only one sheet.") 
                    self.console_instance.consoleSend("green", f"Clean! No other tables were detected")
                return df
            except Exception as e:
                print(f"Error: Unable to read {file_path}. {e}")
                self.console_instance.consoleSend("#CD3333", f"Error: Unable to read {e}")
                return None


    def ReadStartProd(self, ProdDB):
        try:
            encoding = True #self.detect_encoding(ProdDB)
            if encoding:
                ProdDB = self.read_file(ProdDB, "prod")#, encoding=encoding)
                print("Reading prod...")
                self.console_instance.consoleSend("green", "Succesfully red prod!")
            else:
                print(f"Error: Unable to determine encoding for {ProdDB}.")
                self.console_instance.consoleSend("#CD3333", f"Error reading prod DB: Unable to determine encoding.")
        except Exception as e:
            print(f"Reading error on db prod... {e}")
            self.console_instance.consoleSend("#CD3333", f"ERROR on prod DB issued at: {e}")
        return ProdDB

    def ReadStartClient(self, client_db):
        try:
            encoding = True #self.detect_encoding(ProdDB)
            if encoding:
                client_db = self.read_file(client_db, "client")#, encoding=encoding)
                print("Reading client...")
                self.console_instance.consoleSend("green", "Succesfully red client!")
            else:
                print(f"Error: Unable to determine encoding for {client_db}.")
                self.console_instance.consoleSend("#CD3333", f"Error reading client DB: Unable to determine encoding.")
        except Exception as e:
            print(f"Reading error on db client... {e}")
            self.console_instance.consoleSend("#CD3333", f"ERROR on client DB issued at: {e}")
        return client_db

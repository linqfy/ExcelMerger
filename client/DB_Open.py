import pandas as pd
import chardet
from Util.NTF_Manage import GlobalNotificationHandler as Notifications


class Reader:
    def __init__(self, window, console):
        self.window = window
        self.console_instance = console
    
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

    def read_file(self, file_path):
        #try:
            #pass
            #encoding = self.detect_encoding(file_path)
            #df = pd.read_csv(file_path, encoding=encoding)
            #return df
        #except pd.errors.ParserError as e:
            try:
                self.console_instance.consoleSend("#DFFF00", f"Encoding service worker online!")
                encoding = self.detect_encoding(file_path)
                df = pd.read_excel(file_path)#, encoding=encoding)
                return df
            except Exception as e:
                print(f"Error: Unable to read {file_path}. {e}")
                self.console_instance.consoleSend("#CD3333", f"Error: Unable to read {e}")
                return None


    def ReadStartProd(self, ProdDB):
        try:
            encoding = True #self.detect_encoding(ProdDB)
            if encoding:
                ProdDB = self.read_file(ProdDB)#, encoding=encoding)
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
                client_db = self.read_file(client_db)#, encoding=encoding)
                print("Reading client...")
                self.console_instance.consoleSend("green", "Succesfully red client!")
            else:
                print(f"Error: Unable to determine encoding for {client_db}.")
                self.console_instance.consoleSend("#CD3333", f"Error reading client DB: Unable to determine encoding.")
        except Exception as e:
            print(f"Reading error on db client... {e}")
            self.console_instance.consoleSend("#CD3333", f"ERROR on client DB issued at: {e}")
        return client_db

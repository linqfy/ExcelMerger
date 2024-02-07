import os
import csv
import json
from datetime import datetime
from Util.NTF_Manage import GlobalNotificationHandler as Notifications
from tqdm import tqdm
f = open('config.json')
data = json.load(f)

class MDOos:
    def integrityCheck(self) -> bool:
        self.console_instance.consoleSend("#DFFF00", f"Starting cache integrity check")
        
        if not os.path.exists(self.file1):
            self.console_instance.consoleSend("#CD3333", f"FATAL ERROR: No {self.file1}")
            print(f"The file '{self.file1}' does not exist.")
            return False
        
        if not os.path.exists(self.file2):
            self.console_instance.consoleSend("#CD3333", f"FATAL ERROR: No {self.file2}")
            print(f"The file '{self.file2}' does not exist.")
            return False
        
        try:
            # Open the file in binary mode to check if it has content
            with open(self.file1, 'rb') as file:
                first_byte = file.read(1)
                if not first_byte:
                    print(f"The file '{self.file1}' is empty.")
                    return False
            with open(self.file2, 'rb') as file:
                first_byte = file.read(1)
                if not first_byte:
                    print(f"The file '{self.file2}' is empty.")
                    
        except Exception as e:
            print(f"Error reading files: {e}")
            self.console_instance.consoleSend("#CD3333", f"Error reading files: {e}")
            return False
        # If the file exists and has content
        self.console_instance.consoleSend("green", f"Good to go!")
        return True

    def searchIssuesCSV(self, pd_Name_Column, cl_Name_Column, cl_SKU_Column, pd_SKU_Column) -> list:
        self.console_instance.consoleSend("#DFFF00", f"Starting Main worker looking for UPC")
        fixQueue = []
        self.counter = 0
        self.found = 0
        self.total = 0
        self.tested = 0
        
        with open(self.file1, 'r') as file:
            # Create a CSV reader object
            
            self.csv_reader = csv.reader(file)
            
            # Read and print the header
            
            header = next(self.csv_reader)
            print("CSV Header:", header, "\nProd Vars | ", pd_Name_Column, pd_SKU_Column, "\nSKU", cl_Name_Column, cl_SKU_Column)
            
            # Read and print only the lines with missing UPC
            with open(self.file1, 'r') as file1:
                self.csv_reader = csv.reader(file1)
                for row in self.csv_reader:
                    self.total = self.total + 1
                    if not row[pd_SKU_Column]:
                        self.counter = self.counter + 1
                        #print("Current target:", row[self.pd_Name_Column])
                    
                        with open(self.file2, 'r') as file2:
                            self.csv_reader_DB = csv.reader(file2)
                            for lines in self.csv_reader_DB:
                                self.tested = self.tested + 1
                                #print("Searching now on client | Name:", lines[self.cl_Name_Column], "SKU", lines[self.cl_SKU_Column])
                                #print(" BETTER DEBUG Prod Vars  | ", row[pd_Name_Column], row[pd_SKU_Column], "SKU", lines[cl_Name_Column], lines[cl_SKU_Column])
                                if lines[cl_Name_Column] == row[pd_Name_Column]:
                                    #print('v1')
                                    try:
                                        self.console_instance.consoleSend("green", f"UPC: {row[pd_Name_Column]} | {lines[cl_SKU_Column]}")
                                        print(f"Found UPC for UPC: {row[pd_Name_Column]} | ({lines[cl_SKU_Column]})")
                                        self.counter = self.counter - 1
                                        self.found = self.found + 1
                                        fixQueue.append([row[pd_Name_Column], lines[cl_SKU_Column], self.total])
                                    except Exception as e:
                                        print("MALFUNTION 54", e)
                                        exit()
            print("Total:", self.total, "Broken:", self.counter, "Fixed:", self.found, "Tested:", self.tested)
        return fixQueue

    def fixDB(self, fixList, date, pd_SKU_Column, outputName, data) -> bool:
        self.console_instance.consoleSend("#DFFF00", f"Adding UPC's")
        # Open the CSV file and read its contents
        with open(self.file1, 'r', newline='') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            
            # Read all rows into a list
            dataF = list(csv_reader) # DATAF = ROW
        for item in fixList: # LINE = item
            # Check if the specified row_to_edit and column_to_edit are within the range of the data
            if True:
                # Modify the specific element
                dataF[item[2]][pd_SKU_Column] = str(int(item[1]))  # Replace with your desired value
                print(f"Row {item[2] + 1} has been successfully edited.")
                self.console_instance.consoleSend("green", f"Row: edited {item[1]}")
            else:
                print("Invalid row index.")

        # Write the updated data back to the CSV file
        with open((outputName+f'-{date}.csv'), 'w', newline='') as file1:
            # Create a CSV writer object
            csv_writer = csv.writer(file1)
            if bool(data["fixIssuesNumbers"]) == True:
                print("remove processing")
                self.console_instance.consoleSend("#DFFF00", f"Parser Fix on..")
                for row in dataF:
                    if len(row) > 1:
                        # Check if the value in column 1 has at least 2 characters
                        if len(row[pd_SKU_Column]) >= 5:
                            # Remove the last two characters from the value in column 1
                            row[pd_SKU_Column] = row[pd_SKU_Column][:-2]
                            # Write the modified data to the CSV file
            csv_writer.writerows(dataF)
            return True
            
    def __init__(self, console):
        self.console_instance = console
        self.file1 = "cache/cachePROD.csv"
        self.file2 = "cache/cacheCLIENT.csv"
        self.config = data
        self.outputName = str(self.config["OutputName"])
        self.cl_SKU_Column = int(self.config["CL_SKU-Column"]) # LINE 1
        self.pd_SKU_Column = int(self.config["PD_SKU-Column"]) # ROW 1
        self.cl_Name_Column = int(self.config["CL_Name-Column"]) # LinE 0
        self.pd_Name_Column = int(self.config["PD_Name-Column"]) # ROW 0
        

    def startWorker(self):
        f = open('config.json')
        data = json.load(f)
        outputName = str(data["OutputName"])
        cl_SKU_Column = int(data["CL_SKU-Column"]) # LINE 1
        pd_SKU_Column = int(data["PD_SKU-Column"]) # ROW 1
        cl_Name_Column = int(data["CL_Name-Column"]) # LinE 0
        pd_Name_Column = int(data["PD_Name-Column"]) # ROW 0
        fixingList = []
        
        Notifications.push('Estado', "Estamos procesando tu archivo")
        if not self.integrityCheck():
            self.console_instance.consoleSend("#CD3333", f"Error reading files")
            Notifications.push('Estado', "Error! mire la consola")
            return False
        print("Les goooooooo")
        fixingList = self.searchIssuesCSV(pd_Name_Column, cl_Name_Column, cl_SKU_Column, pd_SKU_Column)
        print("gotta fix", fixingList)
        if self.fixDB(fixingList, datetime.now().strftime("%Y-%m-%d-%H_%M_%S"), pd_Name_Column, outputName, data):
            self.console_instance.consoleSend("green", f"-- Worker offline (task completed!)--")
            return True
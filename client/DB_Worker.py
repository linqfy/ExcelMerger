import os
import csv
import json
from datetime import datetime
from Util.NTF_Manage import GlobalNotificationHandler as Notifications
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

    def searchIssuesCSV(self) -> list:
        self.console_instance.consoleSend("#DFFF00", f"Starting Main worker looking for UPC")
        self.fixQueue = []
        self.counter = 0
        self.found = 0
        self.total = 0
        
        with open(self.file1, 'r') as file:
            # Create a CSV reader object
            self.csv_reader = csv.reader(file)
            
            # Read and print the header
            header = next(self.csv_reader)
            print("CSV Header:", header)
            
            # Read and print only the lines with missing UPC
            with open(self.file2, 'r') as file2:
                self.csv_reader_DB = csv.reader(file2)
                for row in self.csv_reader:
                    self.total = self.total + 1
                    if not row[1]:
                        self.counter = self.counter + 1
                        """
                        print("Nombre:", row[0])
                        print("UPC is missing!")
                        print("Artista:", row[2])
                        print("--------")
                        """
                        print("Searching in DB...")
                    
                        for lines in self.csv_reader_DB:
                            #print("Searching now", lines[0])
                            try:
                                if lines[0] == row[0]:
                                    self.console_instance.consoleSend("green", f"UPC: {row[0]} | {lines[1]}")
                                    print(f"Found UPC for UPC: {row[0]} | ({lines[1]})")
                                    self.counter = self.counter - 1
                                    self.found = self.found + 1
                                    self.fixQueue.append([row[0], lines[1], self.total])
                                    break
                            except:
                                print(f"UPC not found for UPC: {row[0]}")
                                self.console_instance.consoleSend("crimson", f"UPC not found for UPC: {row[0]}")
        print("Total:", self.total, "Broken:", self.counter, "Fixed:", self.found)
        return self.fixQueue

    def fixDB(self, fixList, date) -> bool:
        self.console_instance.consoleSend("#DFFF00", f"Adding UPC's")
        # Open the CSV file and read its contents
        with open(self.file1, 'r', newline='') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            
            # Read all rows into a list
            dataF = list(csv_reader)
        for item in fixList:
            # Check if the specified row_to_edit and column_to_edit are within the range of the data
            if True:
                # Modify the specific element
                dataF[item[2]][1] = str(int(item[1]))  # Replace with your desired value
                print(f"Row {item[2] + 1} has been successfully edited.")
                self.console_instance.consoleSend("green", f"Row: edited {item[1]}")
            else:
                print("Invalid row index.")

        # Write the updated data back to the CSV file
        with open((self.outputName+f'-{date}.csv'), 'w', newline='') as file1:
            # Create a CSV writer object
            csv_writer = csv.writer(file1)
            if bool(self.config["fixIssuesNumbers"]) == True:
                print("removing processing")
                self.console_instance.consoleSend("#DFFF00", f"Parser Fix on..")
                for row in dataF:
                    if len(row) > 1:
                        # Check if the value in column 1 has at least 2 characters
                        if len(row[1]) >= 5:
                            # Remove the last two characters from the value in column 1
                            row[1] = row[1][:-2]
                            # Write the modified data to the CSV file
            csv_writer.writerows(dataF)
            return True
            
    def __init__(self, console):
        self.console_instance = console
        self.file1 = "cache/cachePROD.csv"
        self.file2 = "cache/cacheCLIENT.csv"
        self.config = data
        self.outputName = str(self.config["OutputName"])

    def startWorker(self):
        Notifications.push('Estado', "Estamos procesando tu archivo")
        if not self.integrityCheck():
            self.console_instance.consoleSend("#CD3333", f"Error reading files")
            Notifications.push('Estado', "Error! mire la consola")
            return False
        print("Les goooooooo")
        self.fixingList = self.searchIssuesCSV()
        print("gotta fix", self.fixingList)
        if self.fixDB(self.fixingList, datetime.now().strftime("%Y-%m-%d-%H_%M_%S")):
            self.console_instance.consoleSend("green", f"-- Worker offline (task completed!)--")
            return True
import os.path
import csv
from csv import reader
import pandas as pd
import shutil


class DB:

    # default constructor
    def __init__(self):
        self.record = self.config = self.data = self.data_f = self.overflow = None
        self.numBytes = self.maxState = self.maxCity = self.maxUni = self.num_record = self.num_overflow = self.rowLen = 0
        self.removeSpace = self.addSpace = self.removeSpaceCity = self.middle = 0
        self.openCalled = self.found = False

    # create a database
    def createDB(self):
        inputfile = input("Please enter CSV file\n")
        #Chceks to see if csv file exist or not
        if os.path.exists(inputfile):
            print("\n\n\t\tCREATING DATABASE\n\n")
            #Stores the triplet file names into variables
            self.config = inputfile[:-3] + "config"
            self.data_f = inputfile[:-3] + "data"
            self.overflow = inputfile[:-3] + "overflow"
            # Removes the data file that already exist
            if (os.path.exists(inputfile[:-3] + "data")):
                os.remove(inputfile[:-3] + "data")

            # Reads row and finds max length for each field
            with open(inputfile, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if (len(row[1]) > self.maxState):
                        self.maxState = len(row[1])
                    if (len(row[2]) > self.maxCity):
                        self.maxCity = len(row[2])
                    if (len(row[3]) > self.maxUni):
                        self.maxUni = len(row[3])
            # Reads row and writes record
            with open(inputfile, 'r') as read_obj2:
                csv_reader2 = reader(read_obj2)
                for row1 in csv_reader2:
                    self.writeRecord(row1, self.data_f)

            # creates overflow file
            with open(self.overflow, 'w', newline='') as writer_obj:
                pass

            # Creates config file
            with open(self.config, 'w', newline='') as writer_obj:
                pass
        else:
            print("\n\t\tCSV file does not exist in the directory\n")

    # Write record
    def writeRecord(self, info, outfile):
        #Updates the fixed length for each of the records fields
        info[1] += '-' * (self.maxState - (len(info[1])))
        info[2] += '-' * (self.maxCity - len(info[2]))
        info[3] += '-' * (self.maxUni - len(info[3]))
        #Find row length that is used for where we find a record
        self.rowLen = len(info[0]) + len(info[1]) + len(info[2]) + len(info[3]) + 5
        with open(outfile, 'a', newline='') as writer_obj:
            writer = csv.writer(writer_obj)
            writer.writerow(info)

    # Open Database
    def openDB(self, filename):
        #Makes sure the database is not already open
        print("\n\n\t\tOPENING DATABASE...\n\n")
        if self.openCalled == False:
            #Updates the triplet file variables to hold the filenames and sets open to true
            self.data_f = filename[:-6] + "data"
            self.overflow = filename[:-6] + "overflow"
            self.config = filename
            self.openCalled = True
            #Reads the data file to find max length and increment num_record
            with open(self.data_f, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    self.num_record += 1
                    self.rowLen = len(row[0]) + len(row[1]) + len(row[2]) + len(row[3]) + 5
                    self.maxState = len(row[1])
                    self.maxCity = len(row[2])
                    self.maxUni = len(row[3])
            #Reads through the overflow to increment number of overflow records
            with open(self.overflow, 'r') as read_obj2:
                csv_reader2 = reader(read_obj2)
                for row1 in csv_reader2:
                    self.num_overflow += 1
            #Writes to the config file with number of records and overflow records
            with open(filename, 'w', newline='') as writer_obj:
                writer = csv.writer(writer_obj)
                writer.writerow(["Number of Records", "Number of Overflow"])
                writer.writerow([self.num_record, self.num_overflow])
            print("\t\tSUCCESSFUL\n\n")
        else:
            print("\t\tFAILED. CLOSE CURRENT DATABASE\n\n")

    # Checks if open
    def isOpen(self):
        return self.openCalled

    # Close Database
    def closeDB(self, filename):
        print("\n\n\t\tCLOSING DATABASE...\n\n")
        #Resets number of records and overflow records to 0 in config file and sets openCalled to false
        with open(filename, 'w', newline='') as writer_obj:
            writer = csv.writer(writer_obj)
            writer.writerow(["Number of Records", "Number of Overflow"])
            self.num_record = self.num_overflow = 0
            writer.writerow([self.num_record, self.num_overflow])
        self.openCalled = False

    # Get record method
    def getRecord(self, recordNum,file,recordCount):

        self.data = open(file, 'r')
        self.flag = False
        id = state = city = college = "None"
        #Makes sure record number is in range
        if recordNum >= 0 and recordNum < recordCount:
            self.data.seek(0, 0)
            #Finds the row for the record being looked at
            self.data.seek(recordNum * self.rowLen)
            line = self.data.readline().rstrip('\n')
            self.flag = True

        self.data.close()

        #Parses string to store the values into variables
        if self.flag:
            id, state, city, college = line.split(",")
        #Stores the values parsed into a dictionary
        self.record = dict({"ID": id, "State": state, "City": city, "College": college})

    # Binary Search by record id
    def binarySearch(self, input_ID,file,recordCount):
        low = 0
        high = recordCount- 1
        self.found = False

        while high >= low:
            self.middle = (low + high) // 2
            self.getRecord(self.middle,file,recordCount)
            #stores ID from dictionary into mid_id
            mid_id = self.record["ID"]
            #Makes sure the input_id is an integer before undergoing binary search
            try:
                id = int(input_ID)
            except ValueError:
                print("\n\n\t\tEnter integer value for ID\n\n")
                break
            #If middle id matches input_id
            if int(mid_id) == int(input_ID):
                self.found = True
                break
            elif int(mid_id) > int(input_ID):
                high = self.middle - 1
            elif int(mid_id) < int(input_ID):
                low = self.middle + 1
    #Linear Search for overlfow
    def linearSearch(self,file,id):
        self.found = False
        with open(self.overflow,'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                if row[0] == id:
                    self.found = True
                    self.record = dict({"ID": id, "State": row[1], "City": row[2], "College": row[3]})

    # Add record (code for part 2 not 1)
    def addRecord(self, id, state, city, uni):
        print("\n\n\t\tADDING RECORD TO OVERFLOW FILE\n\n")
        #Makes sure the id is not larger than 6 characters and truncates to first 6 if it is
        if len(id) > 6:
            id = id[:-(len(id) - 6)]
        self.writeRecord([id, state, city, uni], self.overflow)
        self.num_overflow += 1
        with open(self.config, 'w', newline='') as writer_obj:
            writer = csv.writer(writer_obj)
            writer.writerow(["Number of Records", "Number of Overflow"])
            writer.writerow([self.num_record, self.num_overflow])

    # Deletes Record (code for part 2 not 1)
    def deleteRecord(self, id):
        #Creates a new copytemp.data file
        with open("copytemp.data",'w') as temp:
            pass

        #Checks to see if the record exists, and if so whether its in overflow or data file
        self.binarySearch(id,self.data_f,self.num_record)
        if self.found:
            file = self.data_f
        else:
            self.linearSearch(self.overflow,id)
            if self.found:
                file = self.overflow
        if self.found:
            print("\n\n\t\tDELETING RECORD\n\n")
            #Copies the data file to the copy file
            shutil.copyfile(file,"copytemp.data")
            #Deletes the current data file
            if os.path.exists(file):
                os.remove(file)
            #Makes sure the file is created in case deleted record is last record in file
            with open(file, 'w') as temp:
                pass
            #Reads the copy file and find where the id of the seeked record to delete and simpy
            #does not append that record to the new data file
            with open("copytemp.data", 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[0] != id:
                        self.writeRecord(row,file)
            #Updates the config file by removing a record
            if file == self.data_f:
                self.num_record -= 1
            else:
                self.num_overflow -= 1
            with open(self.config, 'w', newline='') as writer_obj:
                writer = csv.writer(writer_obj)
                writer.writerow(["Number of Records", "Number of Overflow"])
                writer.writerow([self.num_record, self.num_overflow])
        else:
            print("\n\n\t\tRECORD NOT FOUND\n\n")
        os.remove("copytemp.data")

    # #Updates record (code for part 2 not 1)
    def updateRecord(self, id, state, city, uni):
        # Creates a new copytemp.data file
        with open("copytemp.data", 'w') as temp:
            pass
        # Checks to see if the record exists, and if so whether its in overflow or data file
        self.binarySearch(id, self.data_f, self.num_record)
        if self.found:
            file = self.data_f
        else:
            self.linearSearch(self.config,id)
            if self.found:
                file = self.overflow
        if self.found:
            print("\n\n\t\tUPDATING RECORD\n\n")
            # Copies the data file to the copy file
            shutil.copyfile(file, "copytemp.data")
            # Deletes the current data file
            if os.path.exists(file):
                os.remove(file)
            # Makes sure the file is created in case deleted record is last record in file
            with open(file, 'w') as temp:
                pass
            # Reads the copy file and find where the id of the seeked record to delete and simpy
            # does not append that record to the new data file
            with open("copytemp.data", 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[0] != id:
                        self.writeRecord(row,file)
                    else:
                        self.writeRecord([id,state,city,uni],file)
        os.remove("copytemp.data")

    #Create Report (code is not final and is for part2)
    def createReport(self):
        print("\n\n\t\tCREATING REPORT\n\n")
        df = pd.DataFrame()
        df = pd.read_csv(self.data_f,names=["ID", "State", "City", "University"])
        print(df.head(10))

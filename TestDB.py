from Database import DB
import os
DB = DB()
choice = 0
while choice != "9":
    choice = input("1)Create new database\n"
                   "2)Open Database\n"
                   "3)Close Database\n"
                   "4)Display Record\n"
                   "5)Add Record\n"
                   "6)Delete Record\n"
                   "7)Update Record\n"
                   "8)Create Report\n"
                   "9)Quit\n")
    #Creates Database
    if (choice == "1"):
        DB.createDB()
    #Opens Database
    elif (choice == "2"):
        open = input("\nWhat database would you like to open\n") + ".config"
        if os.path.exists(open) and os.path.exists(open[:-6] + "data"):
            DB.openDB(open)
        else:
            print("\n\t\tNo such database exists.\n")
    #Closes Database
    elif (choice == "3"):
        close = input("What database would you like to close") + ".config"
        if os.path.exists(close):
            DB.closeDB(close)
        else:
            print("\n\n\t\tNo such database exists.\n\n")
    #Displays Record
    elif (choice == "4"):
        if DB.openCalled != False:
            record = input("What record would you like to display?")
            DB.binarySearch(record,DB.data_f,DB.num_record)
            if DB.found:
                print("\n\n\t\tID: " + DB.record["ID"])
                print("\t\tState: " + DB.record["State"])
                print("\t\tCity: " + DB.record["City"])
                print("\t\tCollege: " + DB.record["College"] + "\n\n")
            else:
                DB.linearSearch(DB.overflow,record)
                if DB.found:
                    print("\n\n\t\tID: " + DB.record["ID"])
                    print("\t\tState: " + DB.record["State"])
                    print("\t\tCity: " + DB.record["City"])
                    print("\t\tCollege: " + DB.record["College"] + "\n\n")
                else:
                    print("\n\n\t\tThere is no such record in overflow or data file\n\n")
        else:
            print("\n\n\t\tOpen database first\n\n")
    #Adds Record to Overflow
    elif (choice == "5"):
        if DB.openCalled:
            id = input("Enter the id")
            state = input("Enter the state")
            city = input("Enter the city")
            uni = input("Enter the University")
            DB.addRecord(id,state,city,uni)
        else:
            print("\n\n\t\tOpen a database first\n\n")
    #Deletes Record
    elif (choice == "6"):
        if DB.openCalled:
            id = input("What record would you like to delete? Enter its id")
            DB.deleteRecord(id)
        else:
            print("\n\n\t\tOpen a database first\n\n")
    #Updates Record
    elif (choice == "7"):
        if DB.openCalled:
            id = input("What record would you like to update? Enter its id")
            state = input("What would you like to update the state to?")
            city = input("What would you like to update the city to?")
            uni = input("What would you like to update the University to?")
            DB.updateRecord(id,state,city,uni)
        else:
            print("\n\n\t\tOpen a database first\n\n")
    #Creates Report of first 10 records
    elif (choice == "8"):
        if DB.openCalled:
            DB.createReport()
        else:
            print("\n\n\t\tOpen a database first\n\n")
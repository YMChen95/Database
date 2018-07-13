# CMPUT291 B1 GROUP PROJECT 1
# INSTRUCTOR: Yuan Li Yan
#
# Submitted by: YANG, Chuan 1421992
# CHEN, Mengyang 1412408
# FU, Ruilin 1447466
#
#
# i.e. all data need to be verified before commit to the database

import cx_Oracle #Database manipulation
import sys #exit from python
import os #clear screen
import getpass #implicitly collect password input
import random #

global cursor #global varible declaration 

# Prompt user to enter password, using getpass moudle to avoid echoing password.
def get_pass(): 
    user = input("Username [%s]: " % getpass.getuser())
    pw = getpass.getpass()
    return user,pw

# Exit the program when the user required to do so.
# Param signed_in=0 for exit before connect to SQL Server
# signed_in=1 for exit after connected to SQL Server
def exit(signed_in=0): 
    if signed_in == 1:
        cursor.close()
        con.close()
        sys.exit()
    else:
        sys.exit()
    return 

# Print main menu for the program
# The screen is cleared to improve readability
# cmd--user command at this layer of menu
def main_menu():
    os.system('clear')
    print('Welcome to Auto Reistration System')
    print('Input the following number for features')
    print('1.New Vehicle Registration')
    print('2.Auto Transaction')
    print('3.Driver License Registration')
    print('4.Violation Record')
    print('5.Search Engine')
    print('0.Exit Program')
    cmd = input('Please enter your choice: ')
    if cmd not in {'0','1','2','3','4','5'}:
        print('Invalid input, please try again!')
        cmd = input('Please enter your choice: ')
    if cmd == '0':
        exit(1)
    elif cmd == '1':
        NVR_main()
        main_menu()
    elif cmd == '2':
        AT_main()
        main_menu()
    elif cmd == '3':
        DLR_main()    
        main_menu()
    elif cmd == '4':
        VR_main()
        main_menu()
    elif cmd == '5':
        SE_main()
        main_menu()
    else:
        main_menu()

# Print menu for search engine features
# cmd--note that only user-input command using cmd
# all other data used for SQL queries should use identifiable name
# cmd2, cmd3, etc. for sub-menus
def SE_main():
    os.system('clear')
    print('Input numbers to open a new search')
    print('1.Search a person and license information')
    print('2.Search violation records made by a person')
    print('3.Search vehicle history')
    print('4.Back to main menu')
    cmd = input('Input your choice and press Enter to continue:')
    if cmd == '1':
        os.system('clear')
        print('Search for a person')
        print('1a.Search by driver license no')
        print('1b.Search by name')
        print('1c.Back to the Search Engine menu')
        cmd2 = input('Input your choice and press Enter to continue:')
        if cmd2 == '1a':
            SE_p_license()
        elif cmd2 == '1b':
            SE_p_name()
        elif cmd2 == '1c':
            SE_main()
        else:
            os.system('clear')
            print('Your input is an invalid command.')
            SE_main()#Please note that if there's an invalid input, 
            # rolling back should never accross different layers of menus! 
    elif cmd == '2':
        os.system('clear')
        print('Search for violation records')
        print('2a.Search by drive license no')
        print('2b.Search by SIN')
        print('2c.Back to the Search Engine menu')
        cmd2 = input('Input your choice and press Enter to continue:')
        if cmd2 == '2a':
            SE_v_license()
        elif cmd2 == '2b':
            SE_v_sin()
        elif cmd2 == '2c':
            SE_main()
        else:
            os.system('clear')
            print('Your input is an invalid command.')
            SE_main()
    elif cmd == '3':
        os.system('clear')
        SE_vh()
    elif cmd == '4':
        main_menu()
    else:
        os.system('clear')
        print('Your input is invalid.')
        SE_main()

#Searching Personal Information by Drive License Number
def SE_p_license():
    print("Search Engine --- Personal Information")
    print("Enter a driver's LICENSE NUMBER to start a new search")
    print("Enter Q to back to search menu")
    license_no = input('Enter the license number here and press Enter: ')
    if license_no == "q" or license_no == "Q":
        SE_main()    
    try:
        var = int(license_no)
        # Legimate number check, same as the following
    except ValueError:
        print('Your input is not even a number!!!')
        cmd3 = input('Press Enter to start a new search, press Q to return')
        if cmd3 == 'Q' or cmd3 == 'q':
            SE_main()
        else:
            SE_p_license()   
    if len(license_no) <= 15:# Legimate length check, same as the following 
        statement = "SELECT DISTINCT p.name, dl.licence_no, p.addr, p.birthday,\
        dl.class, dc.description, dl.expiring_date FROM people p, drive_licence\
        dl, driving_condition dc,restriction r WHERE dl.licence_no = '%s' and\
        p.sin = dl.sin and r.licence_no = dl.licence_no and r.r_id = dc.c_id"\
            % license_no
        cursor.execute(statement)
        result = cursor.fetchall()
        if len(result) == 0:# Handling non-exist cases
            print("The license number you entered doesn't match any result \
            in the database")
            cmd3 = input('Press Enter to search again.')
            SE_p_license()
        else:
            count = 0
            for column in result:
                print("This is entry " + str(count+1) + "============")
                print("Name: %s \n, Licence Number: %s \n, Address: %s \n, \
                Birthday: %s \n, Description: %s \n, Type: %s \n, Expiry Date: \
                %s" %(column[0].strip(), column[1].strip(), column[2].strip(),\
                      column[3].strftime("%b-%d-%Y"), column[4].strip(), \
                      column[5].strip(), column[6].strftime("%b-%d-%Y")))
                      #str.strip() to remove excessive spaces around string
                      #date.strftime() forcely convert to readable time format
                count += 1
                # Still need count here, for cases like:
                # One ID, one name, multiple remarks on d_license
            cmd3 = input("Press Enter to get back.")
            SE_main()
    else:# Handling invalid length in user input, same as the following
        print("Invalid License Number!")
        cmd3 = input("Press Enter to continue")
        SE_p_license()
    return

# Searching Personal Info by entering a name
# Please note that this function will only return exact match results
# i.e. NOT regular expression search
# case sensitive is handled. Assuming no entry would be able to store a combination of 
# upper and lower case like "Tony"
def SE_p_name():
    print("Search Engine --- Personal Information")
    print("Enter a driver's NAME to start a new search")
    print("Enter Q to back to search menu")
    name = input('Enter the name here and press Enter: ')
    if name == "q" or name == "Q":
        SE_main()
    elif len(name) <= 40:
        statement = "SELECT dl.licence_no FROM drive_licence dl, people p WHERE p.sin = dl.sin AND p.name = '%s'" % name.lower()
        # A search to obtaining license number have to finish before 
        # 'aligning' each of the rows in different tables for output
        cursor.execute(statement)
        dl_result = cursor.fetchall()
        if len(dl_result) == 0:
            print("The name you entered doesn't match any result in \
            the database")
            cmd3 = input('Press Enter to search again.')
            SE_p_name()
        count = 0
        for license_no in dl_result:
            statement = "SELECT DISTINCT p.name, dl.licence_no, p.addr, p.birthday,\
        dl.class, dc.description, dl.expiring_date FROM people p, drive_licence\
        dl, driving_condition dc,restriction r WHERE dl.licence_no = %s and\
        p.sin = dl.sin and r.licence_no = dl.licence_no and r.r_id = dc.c_id"\
            % license_no
            # The real search here -- using license_no obtained in dl_result 
            cursor.execute(statement)
            result = cursor.fetchall()
            for column in result:
                print("This is entry " + str(count+1) + "============")
                print("Name: %s \n, Licence Number: %s \n, Address: %s \n, \
                Birthday: %s \n, Description: %s \n, Type: %s \n, Expiry Date: \
                %s" %(column[0].strip(), column[1].strip(), column[2].strip(),\
                      column[3].strftime("%b-%d-%Y"), column[4].strip(), \
                      column[5].strip(), column[6].strftime("%b-%d-%Y")))
                count += 1
            cmd3 = input("Press Enter to get back. ")
            SE_main()
    else:
        print("Invalid Name!")
        cmd3 = input("Press Enter to continue")
        SE_p_name()
    return

#Searching violation history by entering licecnse number
def SE_v_license():
    print("Search Engine --- Violation Record")
    print("Enter a driver's LICENSE NUMBER to start a new search")
    print("Enter Q to back to search menu")
    license_no = input('Enter the license number here and press Enter: ')
    if license_no == "q" or license_no == "Q":
        SE_main()    
    if len(license_no) <= 15:
        statement = "SELECT t.ticket_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions, tt.fine FROM ticket t, ticket_type tt, people p, drive_licence dl WHERE dl.licence_no = %s and p.sin = dl.sin and p.sin = t.violator_no and t.vtype = tt.vtype" % license_no 
        cursor.execute(statement)
        result = cursor.fetchall()
        if len(result) == 0:
            print("The license number you entered doesn't match any result \
in the database")
            cmd3 = input('Press Enter to search again.')
            SE_v_license()
        else:
            count = 0
            for column in result:
                print("This is entry " + str(count+1) + "============")
                print("Ticket Number %s\n, Vehicle Number: %s\n, Office Number: %s\n, Violation Type: %s\n, Viodation Date: %s\n, Place: %s\n, Violation Description: %s\n Fine: %s" % (column[0], column[1].strip(), column[2].strip(), column[3].strip(), column[4].strftime("%b-%d-%Y"), \
                      column[5].strip(), column[6].strip(), column[7]))
                      # Note that float type(i.e. fine) is not applicable for .strip() method
                count += 1
            cmd3 = input("Press Enter to get back.")
            SE_main()
    else:
        print("Invalid License Number!")
        cmd3 = input("Press Enter to continue")
        SE_v_license()
    return

# Searching violation history by a entering a SIN number
def SE_v_sin():
    print("Search Engine --- Violation Record")
    print("Enter a driver's SIN to start a new search")
    print("Enter Q to back to search menu")
    sin = input('Enter the SIN here and press Enter: ')
    if sin == "q" or sin == "Q":
        SE_main()    
    if len(sin) <= 15:
        statement = "SELECT t.ticket_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions, tt.fine FROM ticket t, ticket_type tt, people p, drive_licence dl WHERE dl.sin = '%s' and p.sin = dl.sin and p.sin = t.violator_no and t.vtype = tt.vtype" % sin
        cursor.execute(statement)
        result = cursor.fetchall()
        if len(result) == 0:
            print("The SIN number you entered doesn't match any result \
in the database")
            cmd3 = input('Press Enter to search again.')
            SE_v_sin()
        else:
            count = 0
            for column in result:
                print("This is entry " + str(count+1) + "============")
                print("Ticket Number %s\n, Vehicle Number: %s\n, Office Number: %s\n, Violation Type: %s\n, Viodation Date: %s\n, Place: %s\n, Violation Description: %s\n Fine: %s" % (column[0], column[1].strip(), column[2].strip(), column[3].strip(), column[4].strftime("%b-%d-%Y"), \
                      column[5].strip(), column[6].strip(), column[7]))
                count += 1
            cmd3 = input("Press Enter to get back.")
            SE_main()
    else:
        print("Invalid SIN!")
        cmd3 = input("Press Enter to continue")
        SE_v_sin()
    return

# Searching vehicle transaction history by entering a vehicle
# serial number
# Note that valid number check is now removed for a combination of number
# and characters in the serial number
def SE_vh():
    print('Search Engine --- Transaction Record')
    print('Input a VEHICLE SERIAL NUMBER to start a new search.')
    print("Enter Q to back to search menu")
    sn = input('Enter the Serial Number here and press Enter: ')
    if sn.lower() == 'q': 
        SE_main()
    # The number check for SE_vh() is now removed.
    if len(sn) <= 15:
        statement1 = "SELECT count(DISTINCT asale.transaction_id), avg(asale.price) FROM auto_sale asale, ticket t WHERE asale.vehicle_id = '%s' GROUP BY asale.vehicle_id" % sn
        cursor.execute(statement1)
        result1 = cursor.fetchall()        
        
        if result1 ==[]:
        # Even in empty result the COUNT@sql will return {(0,....)}
        # handle non-existing search here 
            print("The serial number you entered have no transaction record available in this database!")
            cmd3 = input('Press Enter to search again.')
            SE_main()
        else:
            for column in result1:
                print("This is the transaction statistics for vehicle %s " % sn)
                statement = "SELECT count(t.ticket_no) FROM auto_sale asale, ticket t WHERE t.vehicle_id = asale.vehicle_id and t.vehicle_id = '%s' GROUP BY asale.vehicle_id" % sn
                cursor.execute(statement)
                result = cursor.fetchall()
                r = 0
                for i in result:
                    r = i
                    break
                print("Times of Transaction %s\n Average Selling Price: %s\n Overall Violations Involved: %s\n" % (column[0], column[1], r))
                cmd3 = input("Press Enter to get back.")
                SE_main()
    else:
        print("Invalid Serial Number!")
        cmd3 = input("Press Enter to continue")
        SE_vh()
    return

# Main menu for Driver Licence Registration features
def DLR_main():
    print ("Driver Licence Registration")
    print ("----------------------------------")
    print ("1.Registration of New Person")
    print ("2.Registration of New Driver")
    print ("0. Back to the Main Menu")
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except:
            print("Invalid input! Please try again")
        else:
            if (choice > 2) or (choice <0):
                print ("Invalid input! Please try again")
            else:
                break
    
    if choice == 0:
        return 
    if choice == 1:     #Registration of New Person
        reg_person()
    if choice == 2:
        reg_licence()
        
    return                  # return to the main menu

#Adding a new person's row to table PEOPLE in SQL
def reg_person():
    print ("----------------------------------")
    print ("Registration of New Person")    
    while True:     # sin
        sin = input("Please enter the SIN number: ")
        if len(sin) >15:
            print ("Invalid input! Please try again!")
            continue
        else:
            cursor.execute("SELECT people.sin FROM people WHERE people.sin = '%s'" % sin)
            exist = cursor.fetchone()
            if exist == None:   # success
                break   
            else:
                print ("The sin number: "+str(sin)+" has already exsited. Please try agian!")
                continue
            
    while True:     #name
        name = input("Please enter the NAME: ")
        if len(name) > 40:
            print ("Invalid input! Please try again!")
            continue        
        else:
            break
        
    while True:     # height
        try:
            height = float(input("Please enter the HEIGHT(cm): "))
        except :
            print ("Invalid input! Please try again!")
            continue                    
        else:
            if height > 300:        # too high
                print ("Invalid input! Please try again!")
                continue        
            else:
                break        
        
    while True:     # weight
        try:
            weight = float(input("Please enter the WEIGHT(kg): "))
        except :
            print ("Invalid input! Please try again!")
            continue                    
        else:
            break
            
    while True:     # eye color
        eyecolor = input("Please enter the EYECOLOR: ")
        if len(eyecolor) > 10:
            print ("Invalid input! Please try again!")
            continue        
        else:
            break
        
    while True:     # hair color
        haircolor = input("Please enter the HAIRCOLOR: ")
        if len(haircolor) > 10:
            print ("Invalid input! Please try again!")
            continue        
        else:
            break    
    
    while True:     # addr
        addr = input("Please enter the ADDRESS: ")
        if len(addr) > 50:
            print ("Invalid input! Please try again!")
            continue        
        else:
            break        
        
    while True:     # gender
        gender = input("Please enter the GENDER(m/f): ")
        if gender != 'm' and gender != 'f':
            print ("Invalid input! Please try again!")
            continue        
        else:
            break    
        
    while True:     # insert
        date = input("Please enter the BIRTHDAY(DD-MMM-YYYY): ")   
        try:
            b_date = date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] >30 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue   
            else:
                print ("Invalid input! Please try again!")
                continue             
            break

    cursor.execute("INSERT INTO people (SIN,NAME, HEIGHT, WEIGHT, EYECOLOR, HAIRCOLOR, ADDR, GENDER, BIRTHDAY) VALUES ('"
    +str(sin)+"','"+str(name)+"',"+str(height)+","+str(weight)+",'"+str(eyecolor)+"','"+str(haircolor)+"','"+str(addr)+"','"
    +str(gender)+"','"+str(date)+"')")
    con.commit()  

    print("Person successfully added!")
    tmp = input("Press enter to continue...")

    return

# Add a new license using SQL queries
def reg_licence():
    print ("----------------------------------")
    print ("Registration of New Licence")
    
    while True:
        sin = input("Please enter the SIN number of the new driver: ")
        if len(sin) >15:
            print ("Invalid input! Please try again!")
            continue
        else:
            cursor.execute("SELECT people.sin FROM people WHERE people.sin = '%s'" % sin)
            exist = cursor.fetchone()
            if exist == None:  
                print ("The person with SIN: "+str(sin)+" is not in the database")
                while True:
                    c = input("Would you like to add this person to the database(Y/N)? ")
                    if c == 'Y' or c == 'y':
                        reg_person()
                        break
                    elif c == 'N' or c == 'n':
                        print ("Please try again!")
                        break
                    else:
                        print ("Invalid choice! Please try again!")
                        continue
            else:
                cursor.execute("SELECT drive_licence.sin FROM drive_licence WHERE drive_licence.sin = '%s'" % sin)
                d_exist = cursor.fetchone()
                if d_exist == None:
                    break
                else:
                    print ("The person has already got a driver licence! Please try again!")
                    continue

    while True:     # licence_no
        licence = input("Please enter the licence number: ")
        if len(licence) >15:
            print ("Invalid input! Please try again!")
            continue
        else:        
            cursor.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '%s'" % licence)
            exist = cursor.fetchone()
            if exist == None:
                break
            else:
                print ("The person with licence number: "+str(licence)+" has already existed! Please try again")
                continue
        
    while True:
        try :   
            class_lv = int(input("Please enter the class of the driver licence(1-7): "))
        except :
            print ("Invalid Input!Please try agian")
        else:
            if class_lv > 7 or class_lv < 1:
                print ("Invalid Input!Please try agian")
                continue
            else:
                class_lv = 'Class' + str(class_lv)
                break
            
    while True:     # issuing date
        i_date = input("Please enter the issuing date(DD-MMM-YYYY): ")   
        try:
            b_date = i_date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] >30 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue    
            else:
                print ("Invalid input! Please try again!")
                continue                
            break
        
    while True:     # expiring date
        e_date = input("Please enter the expiring date(DD-MMM-YYYY): ")   
        try:
            b_date = e_date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] >30 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue    
            else:
                print ("Invalid input! Please try again!")
                continue                 
            break
    
    while True:
        photo = input("Please enter the name of the photo(include the extension, like *.jpg, etc.): ")
        try:
            f_image = open(photo,'rb')
            break
        except IOError:
            print("File could not be opened. Please try again!")
            continue

    image = f_image.read()        
    
    
    while True:     # driving condition
        d_condition = input("Please enter the driving condition (None for no records): ")
        d_condition = d_condition.lower()
        if len(d_condition) > 1024:
            print ("Invlid input! Please try again!")
        else:
            break
        
    while True:
        c_id = random.randint(0,100000000)
        cursor.execute("SELECT c_id FROM driving_condition WHERE c_id = %d" %c_id)
        exist = cursor.fetchone()
        if exist == None:
            break
    
    cursor.execute("INSERT into DRIVE_LICENCE (LICENCE_NO, SIN, CLASS, PHOTO, ISSUING_DATE, EXPIRING_DATE)"
    +"values (:LICENCE_NO, :SIN, :CLASS, :PHOTO, :ISSUING_DATE, :EXPIRING_DATE)",{'LICENCE_NO':licence,'SIN':sin,'CLASS':class_lv,'PHOTO':image,'ISSUING_DATE':i_date,'EXPIRING_DATE':e_date})  
        
    cursor.execute("INSERT into DRIVING_CONDITION (C_ID,DESCRIPTION) "
    +"values (:C_ID,:DESCRIPTION)", {'C_ID':c_id,'DESCRIPTION':d_condition})

    cursor.execute("INSERT into restriction (LICENCE_NO,R_ID)"
    +"values (:LICENCE_NO,:R_ID)",{'LICENCE_NO':licence,'R_ID':c_id})
    
    print("Licence is successfully registered!")
    tmp = input("Press Enter to continue...")    
    con.commit()    
    f_image.close()


def VR_main():
    print ("Violation Record")
    print ("----------------------------------")   
    print ("1.Registration of New Violation Record")
    print ("0.Back to the Main Menu")
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except :
            print("Invalid input! Please try again")
        else:
            if (choice > 1) or (choice < 0):
                print ("Invalid input! Please try again")
            else:
                break    
    if choice == 0:
        return 
    if choice == 1:     # Registration of New Violation Record
        reg_NVR()
    
    return



def reg_NVR():
    while True:          # get a new ticket number
        ticket_no = random.randint(0,100000000)
        cursor.execute("SELECT t.ticket_no FROM ticket t WHERE ticket_no = %d" %ticket_no)
        exist = cursor.fetchone()
        if exist == None:
            print ("The ticket number is: %d" %ticket_no)
            break  

    while True:         # the violate vehicle number
        vehicle_no = input("Please enter the violated vehicle number: ")
        if len(vehicle_no) >15:
            print ("Invalid input! Please try again!")
            continue
        else:
            cursor.execute("SELECT serial_no FROM vehicle WHERE serial_no = '%s'" % vehicle_no)
            exist = cursor.fetchone()
            if exist == None:          
                print ("The vehicle with serial_no: %s is not in our database. Please try again!" % vehicle_no)
                continue
            else:
                break            
    
    cursor.execute("SELECT owner_id FROM owner WHERE is_primary_owner = 'y' AND vehicle_id = '%s'" %vehicle_no)
    primary_owner = cursor.fetchone()
    print ("As for the Vehicle with serial number: %s," %vehicle_no)
    print ("The SIN number of the Primary Owner: %s" %primary_owner)
    while True:
        choice1 = input("Would you like to register this violation record for the primary owner (Y/N)? ")
        choice1 = choice1.lower()
        if choice1 != 'y' and choice1 != 'n':
            print("Invalid input! Please try again!")
            continue
        else:
            if choice1 == 'n':    
                while True:         # the violator's SIN
                    violator_no = input("Please enter the SIN number of the violator: ")
                    if len(violator_no) >15:
                        print ("Invalid input! Please try again!")
                        continue
                    else:
                        cursor.execute("SELECT people.sin FROM people WHERE people.sin = '%s'" % violator_no)
                        exist = cursor.fetchone()
                        if exist == None:          
                            print ("The person with SIN: %s doesn't exist. Please try again!" % vioaltor_no)
                            continue
                        else:
                            break
            if choice1 == 'y':
                for i in primary_owner:
                    violator_no = i
            break
                        
            
    while True:           # the officer's SIN
        officer_id = input("Please enter the SIN number of the officer: ")
        if len(officer_id) >15:
            print ("Invalid input! Please try again!")
            continue
        else:
            cursor.execute("SELECT people.sin FROM people WHERE people.sin = '%s'" % officer_id)
            exist = cursor.fetchone()
            if exist == None:          
                print ("The person with SIN: %s doesn't exist. Please try again!" % officer_id)
                continue
            else:
                break        
    
    while True:         # ticket type
        cursor.execute("SELECT * FROM ticket_type")
        exist = cursor.fetchall()             
        print ("Ticket_type")
        print ("--------------------------------")
        ticket_list = []                    
        for row in exist:
            print ("%10s $%.2f" %(row[0].strip(), row[1]))                        
            ticket_list.append(row[0].strip())        
        vtype = input("Please select the ticket type from the above: ")
        if vtype not in ticket_list:
            print("Please enter a Ticket Type from the above")
            continue
        else:
            break
        
    while True:     # violation date
        v_date = input("Please enter the violation date(DD-MMM-YYYY): ")   
        try:
            b_date = v_date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30) or (b_date[0] <= 0):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] > 30 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29 or (b_date[0] <= 0):
                        print ("Invalid input! Please try again!")
                        continue    
            else:
                print ("Invalid input! Please try again!")
                continue             
            break        
        
    while True:     # violation place 
        place = input("Please enter the violation place: ")
        place = place.lower()
        if len(place) > 20:
            print ("Invlid input! Please try again!")
        else:
            break        
        
    while True:     # violation description
        descriptions = input("Please enter the descriptions for the violation: ")
        descriptions = descriptions.lower()
        if len(descriptions) > 1024:
            print ("Invlid input! Please try again!")
        else:
            break        

    cursor.execute("INSERT INTO ticket VALUES ("
                    +str(ticket_no)+",'"+str(violator_no)+"','"+str(vehicle_no)+"','"+str(officer_id)+"','"+str(vtype)+"','"+str(v_date)+"','"+str(place)+"','"+str(descriptions)+"')")    
    
    print("Violation successfully added!")
    tmp = input("Press enter to continue...")
    con.commit()       


def Auto_transacation():
    while True: #get the transaction id and check if it is the only one
        transaction_id=input("Please enter the transaction_id: ")
        try:
            transaction_id=int(transaction_id)
            if is_exist_transaction(transaction_id):
                print("transaction_id already existed, please enter another one")
            else:
                break
        except ValueError:
            print("transaction id must be a number")
    while True:
        vehicle_id=input("Plesse enter the vehicle id: ")
        if(len(vehicle_id)>15):
            print("Please enter a valid input. ")
        else:
            if is_exist_car(vehicle_id):
                break
            else:
                userinput1=input("This vehicle does't register, register it now?(y/n): ").lower()
                if userinput1=='y':
                    NVR_main()
                    continue
                else:
                    print("Plese try again. ")
    
    while True:    
    #Get the seller id(sin) and check if exist this person
    #Check if this seller own that vehicle
        seller_id=input("Please enter the seller_id: ").lower()
        if(len(seller_id)>15):
            print("Please enter a valid input. ")
        else:            
            if is_exist_person(seller_id):
                if is_owner(seller_id):
                    break
                else:
                    print("This person doesn't own this vehicle, try again")
            else:
                print("this person doesn't register.")
            
    while True:
    #Get the primary owner from the buyers
    #Check if this buyer exist
        primary_buyer_id=input("Please enter the primary buyer's id: ")
        if(len(primary_buyer_id)>15):
            print("Please enter a valid input. ")
        else:                
            if is_exist_person(primary_buyer_id):
                break
            else:
                userinput2=input("This person doen't register, register now? (Enter y to continue): ").lower()
                if userinput2=='y':
                    reg_person()
                else:
                    print("Please enter a exist buyer's id. ")
                    
    while True:
    #Get the secondary owner from the buyers
    #Check if those buyers exist    
        buyers=[]
        is_other_buyers=input("Do you want to add a secondary buyer? (Enter y to continue): ").lower()
        if is_other_buyers=='y':
            secondary_buyers_id=input("Please enter the secondary buyer's id: ")
            if is_exist_person(secondary_buyers_id):
                buyers.append(secondary_buyers_id)
            else:
                userinput2=input("This person doen't register, register now? (Enter y to continue): ").lower()
                if userinput2=='y':
                    reg_person()
                    buyer.append(secondary_buyers_id)
                else:
                    print("Please enter a exist buyer's id. ")                
        else:
            break

        
    while True:
    #Get the price
        price=input("Please enter the price : ")
        if( len(price) <= 9):
                    break;
        else:
            print("Error: value too large")

    
    while True:     #Get sale date
        s_date = input("Please enter the sale date(DD-MMM-YYYY): ")   
        try:
            b_date = s_date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31 or b_date[0]<=0):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30 or b_date[0]<=0):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] >29 or b_date[0]<=0:
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29 or b_date[0]<=0:
                        print ("Invalid input! Please try again!")
                        continue   
            else:
                print ("Invalid input! Please try again!")
                continue             
            break        

    #Insert all the values into database
    cursor.execute("DELETE FROM owner WHERE ( owner_id ="+str(seller_id)+")")
    cursor.execute(" insert into auto_sale values('" + str(transaction_id) + "','" + str(seller_id) +"','" + str(primary_buyer_id) + "','" + str(vehicle_id) + "','" + str(s_date) + "','" + str(price) + "')")
    cursor.execute(" insert into owner values('" + str(primary_buyer_id) + "','" + str(vehicle_id) + "','y')")
    
    for i in range(len(buyers)):
        cursor.execute(" insert into owner values('" + str(buyers[i]) + "','" + str(vehicle_id) + "','n')")
    #Value insertion done
    c = input("Press enter to continue...")
    
#Function parts   
def is_exist_transaction(transaction_id):
    cursor.execute("select transaction_id from auto_sale where transaction_id = '"+str(transaction_id)+"'")
    rows=cursor.fetchone()
    if rows==None:
        return False
    else:
        return True
                   
def is_exist_car(serial_no):
    cursor.execute("select serial_no from vehicle where serial_no = '"+serial_no+"'")
    rows = cursor.fetchone()
    if rows==None:
        return False
    else:
        return True    

def is_owner(Id):
    cursor.execute("select owner_id from owner where owner_id = '"+Id+"'")
    rows=cursor.fetchone()
    if rows==None:
        return False
    else:
        return True
def is_exist_person(Id):
    cursor.execute("select sin from people where sin = '"+Id+"'")
    rows=cursor.fetchone()
    if rows==None:
        return False
    else:
        return True
    

def AT_main():
    print ("----------------------------------")
    print ("welcome to Auto sale ")    
    print ("----------------------------------")
    print ("1. Registration for new sale")
    print ("0. Back to the Main Menu")
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except:
            print("Invalid input! Please try again")
        else:
            if (choice > 1) or (choice <0):
                print ("Invalid input! Please try again")
            else:
                break
    
    if choice == 0: #Back to main menu
        return 
    if choice == 1: #Registration of New transaction
        Auto_transacation()  
    return

#=============================================

def New_Vehicle_Registraion():
    primary_owner=[]
    secondary_owner=[]
               
    flag = True
    while flag:
    #get serial number, and check if it is a exist car
        serial_no=input("Enter serial number: ")
        if len(serial_no)>=15 or len(serial_no)<=0:
            print("invalid inputs")
        else:
            if is_exist_car(serial_no):
                print("vehicle already existed, try agian")
            else:
                flag=False

    flag = True
    while flag:
    #get maker
        maker=input("Enter maker: ")
        if len(maker)>=20 or len(maker)<=0:
            print("invalid inputs")
        else:
            flag=False
    
    flag = True    
    while flag:
    #get model
        model=input("Ener model: ")
        if len(model)>=20 or len(model)<=0:
            print("invalid inputs")
        else:
            flag=False
    
    flag = True    
    while flag:
    #get year, check if it's length is four
        try:
            year=int(input("Enter year: "))
        except:
            print("invalid inputs")
        else:
            if year>9999 or year < 1000:
                print("invalid inputs")
            else:
                flag=False
          
    
    flag = True        
    while flag:
    #get color
        color=input("Enter color: ")
        if len(color)>20 or len(color)<=0:
            print("Error")
        else:
            flag=False
    
    #get the vehicle types from database
    cursor.execute("select type, type_id FROM vehicle_type")
    data = cursor.fetchall()
    
    #list store the vehicle type information
    vehicleType={}
    print ("+------------------------------+")
    print ("Vehicle Type from the database is the following")
    print ("+------------------------------+")
    for x,y in data:
        vehicleType[x.lower]=y
        print(x.lower())
    end = True
    while end:
    #get vehicle type for this new vehicle
        print ("+------------------------------+")
        print("Please enter the vehicle types from above list")       
        vtype = input("Please enter the type of the vehicle: ").lower()
        for x,y in data:
            x = x.lower().strip()
            if vtype == x:
                type_id = y
                end = False
                break
        if end: 
            print("Error: invalid vehicle type")    

    flag = True
    while flag:
    #get primary owner and secondary owners
        user_input1=input("Do you want add an owner for this vehicle? (y/n): ").lower()     
        if user_input1=="y":
            owner_id=input("Enter onwer id: ")
            primary=input("Is a primary owner? (y/n): ").lower()        
            if is_exist_person(owner_id):
                if primary =='y'and len(primary_owner)==0:
                    primary_owner.append(owner_id)
                elif primary=='y' and len(primary_owner)==1:
                    print("Error, each vehicle can have at most one primary owner")
                    continue
                elif primary=='n':
                    secondary_owner.append(owner_id)
                else:
                    print(len(primary_owner),primary_owner)
                    print("Error, please try again")
            else:
                print("This person isn't in database, register this person.")
                reg_person()
                if primary =='y'and len(primary_owner)==0:
                    primary_owner.append(owner_id)
                elif primary=='y' and len(primary_owner)==1:
                    print("Error, each vehicle can have at most one primary owner")
                    continue
                elif primary=='n':
                    secondary_owner.append(owner_id)
                else:
                    print("Error, please try again")                
        elif user_input1=="n" and len(primary_owner)==0:
            print("Error, you have to have a primary owner for this vehicle.")
        elif user_input1 =="n" and len(primary_owner)>0:
            flag= False
        else:
            print("Error, please Enter y/n")
        
            
            
             
    try:
        cursor.execute(" insert into vehicle values('" + str(serial_no) + "','" + str(maker) +"','" + str(model) + "'," + str(year) + ",'" + str(color) + "'," + str(type_id) + ")")
    except:
        print("Sql error, try again.")
   
    for i in primary_owner:
        try:
            cursor.execute("insert into owner values('" + str(i) +"','" + str(serial_no) +"','y')")
        except:
            print("sql error, try again. ")
    
    for i in secondary_owner:
        try:
            cursor.execute("insert into owner values('" + str(i) +"','" + str(serial_no) +"','n')")
        except:
            print("sql error, try again. ")    
    # value intsertion done
    print("New vehicle registered successfully. ")
    c = input("Presss Enter to continue...")
    
# Methods to check if a specified car/person exists                   
def is_exist_car(serial_no):
    cursor.execute("select serial_no from vehicle where serial_no = '"+serial_no+"'")
    rows = cursor.fetchone()
    if rows==None:
        return False
    else:
        return True    
def is_exist_person(owner_id):
    cursor.execute("select sin from people where sin = '"+owner_id+"'")
    rows=cursor.fetchone()
    if rows==None:
        return False
    else:
        return True


#Print menu for New Vehicle Registration
def NVR_main():
    print ("New vehicle Registration")
    print ("----------------------------------")
    print ("1. Registration of New vehicle")
    print ("0. Back to the Main Menu")
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except:
            print("Invalid input! Please try again")
        else:
            if (choice > 1) or (choice <0):
                print ("Invalid input! Please try again")
            else:
                break
    
    if choice == 0:     #back to main menu
        return 
    if choice == 1:     #Registration of New vehicle
        New_Vehicle_Registraion()
    return


# Main Program
if __name__ == '__main__':   
    while True:
        try:
            user, pw = get_pass()
            con_string = user + '/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
            # The SQL Server is fixed for demoing
            con = cx_Oracle.connect(con_string)
            con.autocommit = 1
            # Automatic commit Enabled(By defualt off 
            cursor = con.cursor()
            # Cursor is forced to be a global varible, so only one SQL iteration a time 
            break
        except cx_Oracle.Error:# Handle account/network exceptions
            os.system('clear')
            print('Unable to connect to SQL Server.')
            print('Check Internet connection.')
            print('Check username & password.')
            cmd = input('Press Enter to Re-attempt or Q to exit: ')
        if cmd == 'Q' or cmd == 'q':
            exit()
    main_menu()

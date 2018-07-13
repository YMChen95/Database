import sys
import cx_Oracle
import main
import NVR
import DLR

def Auto_transacation():
    while True:
        transaction_id=input("Please enter the transaction_id: ")
        if is_exist_transaction(transaction_id):
            print("transaction_id already existed, please enter another one")
        else:
            break
    
    while True:
        vehicle_id=input("Plesse enter the vehicle id: ")
        if(len(vehilce_id)>15):
            print("Please enter a valid input. ")
        else:
            if is_exist_car(vehicle_id):
                break
            else:
                userinput1=("This vehicle does't register, register it now?(y/n): ").lower()
                if userinpu1=='y':
                    NVR.NVR_main()
                else:
                    print("Plese try again. ")
    
    while True:
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
        primary_buyer_id=input("Please enter the primary buyer's id")
        if(len(primary_buyer_id)>15):
            print("Please enter a valid input. ")
        else:                
            if is_exist_person(primary_buyer_id):
                break
            else:
                userinput2=input("This person doen't register, register now? (Enter y to continue): ").lower()
                if userinput2=='y':
                    DLR.reg_person()
                else:
                    print("Please enter a exist buyer's id. ")
    while True:
        buyers=[]
        is_other_buyers=input("Do you want to add a secondary buyer? (y/n): ")
        if is_other_buyers=='y':
            secondary_buyers_id=input("Please enter the secondary buyer's id")
            if is_exist_person(secondary_buyers_id):
                buyers.append(secondary_buyers_id)
            else:
                userinput2=input("This person doen't register, register now? (Enter y to continue): ").lower()
                if userinput2=='y':
                    DLR.reg_person()
                    buyer.append(secondary_buyers_id)
                else:
                    print("Please enter a exist buyer's id. ")                
        else:
            break

        
    while True:
        price=input("Please enter the price : ")
        if( len(price) <= 9):
                    break;
        else:
            print("Error: value too large")

    
    while True:     # sale date
        s_date = input("Please enter the sale date(DD-MMM-YYYY): ")   
        try:
            b_date = date.split('-')
            b_date[0] = int(b_date[0])
            b_date[1] = b_date[1].lower()
            b_date[2] = int(b_date[2])
        except:
            print ("Invalid input! Please try again!")
        else:
            if b_date[1] in ('jan','mar','may','jul','aug','oct','dec'):
                if (b_date[0] > 31):
                    print ("Invalid input! Please try again!")
                    continue
            elif b_date[1] in ('apr','jun','sep','nov'):
                if (b_date[0] > 30):
                    print ("Invalid input! Please try again!")
                    continue                
            elif b_date[1] == 'feb':
                if b_date[2] % 4 == 0 :
                    if b_date[0] >29:
                        print ("Invalid input! Please try again!")
                        continue
                else:
                    if b_date[0] >29:
                        print ("Invalid input! Please try again!")
                        continue    
            break        


    main.cursor.execute("DELETE FROM owner WHERE (lower owner_id ="+str(seller_id)+")")
    main.cursor.execute(" insert into auto_sale values('" + str(transaction_id) + "','" + str(seller_id) +"','" + str(primary_buyer_id) + "'," + str(vehicle_id) + ",'" + str(s_date) + "'," + str(price) + ")")
    

def is_exist_transaction(transaction_id):
    main.cursor.execute("select transaction_id from auto_sale where transaction_id = '"+transaction_id+"'")
    rows=main.cursor.fetchone()
    if rows==None:
        return True
    else:
        return False
                   
def is_exist_car(serial_no):
    main.cursor.execute("select serial_no from vehicle where serial_no = '"+serial_no+"'")
    rows = main.cursor.fetchone()
    if rows==None:
        return False
    else:
        return True    

def is_owner(Id):
    main.cursor.execute("select owner_id from owner where owner_id = '"+Id+"'")
    rows=main.cursor.fetchone()
    if rows==None:
        return True
    else:
        return False
def is_exist_person(Id):
    main.cursor.execute("select sin from people where sin = '"+Id+"'")
    rows=main.cursor.fetchone()
    if rows==None:
        return False
    else:
        return True
    
    
    
def Auto_sale_main():
    print ("----------------------------------")
    print ("welcome to Auto sale ")    
    Auto_transacation()
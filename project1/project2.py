import os
import sys
import time
import bsddb3 as bsddb
import random
# Make sure you run "mkdir /tmp/my_db" first!
DB_FILE_btree = "/tmp/chuan1_db/btreedb.db"
DB_FILE_hash = "/tmp/chuan1_db/hashdb.db"
DB_FILE_index1 = "/tmp/chuan1_db/index1db.db"
DB_FILE_index2 = "/tmp/chuan1_db/index2db.db"
answerfile = ""

DB_SIZE = 1000
SEED = 10000000

db = ""
db2 = ""


def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))


def populate(type_option,created):
    if created:
        print("Database has already been created!!!")
        input("Press Enter to return Main Menu...")
        return created
    
    create = False          # use to record whether the database has created or not
    
    if create == True:
        print("Database has already been created! ")
        tmp = input("Press Enter to Return Main Menu...")
        return
    # Btree
    if type_option == "btree" :
        print("Database does not exist! And we will create one for you! ")
        db = bsddb.db.DB()
        db.open(DB_FILE_btree, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
            
    # Hash Table
    if type_option == "hash":
        print("Database does not exist! And we will create one for you! ")
        db = bsddb.db.DB()
        db.open(DB_FILE_hash, bsddb.db.DB_HASH, bsddb.db.DB_CREATE)
            
    # IndexFile
    if type_option == "indexfile" :
        print("Database does not exist! And we will create one for you! ")
        db = bsddb.db.DB()
        db.open(DB_FILE_index1, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)        
        db2 = bsddb.db.DB()
        db2.open(DB_FILE_index2, None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
            
    
    # Begin to create the data
          
    random.seed(SEED)    
    
    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        #print (key)
        #print (value)
        #print ("")
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        db.put(key, value)
    
        if type_option == "indexfile":
            db2.put(value, key)
        
        cur = db.cursor()
        iter = cur.first()
        # print the database
        while iter:
            print(iter[0].decode("utf-8"))
            print(iter[1].decode("utf-8"))
            iter = cur.next()
        print("------------------------")
        try:
            db.close()
        except Exception as e:
            print (e)        
          
        create = True       # record that we have created the database  
        print ("Creating Database Done!")
        input("Press Enter to Continue...")
        
        return create

def key_search():
    def Key():
        #Search with given key  
        try:
            db = bsddb.db.DB()
            db.open(DB_FILE)
        except:
            print("Error: no database found. please create database first")
            return
    
        stdin = input("Enter the key Please")
        
        records = 0 
    
        if db.has_key(stdin.encode(encoding='UTF-8')):
            records += 1
            results(stdin,db_1.get(stdin.encode(encoding='UTF-8')).decode(encoding='UTF-8'))        
            
        
        db_1.close()     

def data_search(type_option,create):          # Retrieve records with a given data
    if not create:
        print("Please Create the Database first!!")
        input("Press Enter to Continue....")
        return
    
    global answerfile
    
    if type_option == "btree" :
        db = bsddb.btopen(DB_FILE_btree, "r")
    elif type_option == 'hash' :
        db = bsddb.hashopen(DB_FILE_hash, "r")
    else:
        db2 = bsddb.db.DB()
        db2 = db2.open(DB_FILE_index2)
    
    answer = []             # use to save the keys
    
    data = input("Please input the data that you want to search: ")
    data = data.encode(encoding='UTF-8')
    
    if (type_option != "indexfile"):
        start = time.time()
        for (key, value) in db.iteritems():
            if value == data:
                answer.append(key)
                
        end = time.time()
        duration = end - start 
                
        print ("Time Used :",duration)
        print ("Total number of the searched data is :",len(answer))
        input ("Press Enter to Continue...")
        
        answerfile.write("The keys for data "+str(data.decode(encoding='UTF-8'))+" : \n")
        num = 1
        for i in answer:
            answerfile.write("Key"+str(num)+": "+str(i.decode(encoding='UTF-8'))+"\n")
            answerfile.write("Data: "+str(data.decode(encoding='UTF-8'))+"\n")
            answerfile.write("\n")
            
        answerfile.write("\n"+"\n"+"\n")
            
    else:       # indexfile
        start = time.time()
        
        if db2.has_key(data):
            answer.append(db2.get(data).decode(encoding='UTF-8'))
        
        end = time.time()
        duration = end - start
        
        print ("Time Used :",duration)
        print ("Total number of the searched data is :",len(answer))
        input ("Press Enter to Continue...")
        
        answerfile.write("The keys for data "+str(data.decode(encoding='UTF-8'))+" : \n")
        num = 1
        for i in answer:
            answerfile.write("Key"+str(num)+": "+str(i.decode(encoding='UTF-8'))+"\n")
            answerfile.write("Data: "+str(data.decode(encoding='UTF-8'))+"\n")
            answerfile.write("\n")        
            
    return
# def range_search():
    


def main(argv):
    # Take the Type Option   
    create = False
    type_option = ""        # use to get the type option
    while True:
        try:
            option = argv[1]
        except:
            print("Invalid input! Please try again")
            return
        else:
            if option != "btree" and option != "hash" and option != "indexfile":
                print("Invalid Database! Please try again!")
                return             
            else:
                type_option = option      
                break
            
    
    # Open or Create the Answer File
    try:
        os.chdir("/tmp/chuan1_db")
    except:
        os.mkdir("/tmp/chuan1_db")
                
    global answerfile            
    answerfile = open("answers", "w")
    
    
    # Begin 
    while True:
        # Show the MainMenu
        os.system("clear")
        print ("The database type option :",option) 
        print("1. Create and populate a database")
        print("2. Retrieve records with a given key")
        print("3. Retrieve records with a given data")
        print("4. Retrieve records with a given range of key values")
        print("5. Destroy the database")
        print("0. Quit")
        
        while True:
            try:
                choice = int(input("Please Enter Your Choice >>> "))
            except:
                print("Invalid Input! Please try again!")
                continue
            else:
                if choice >= 0 and choice <= 5:
                    break
                else:
                    print("Invalid Input! Please try again!")  
                    continue
        
        # Cases 
        if choice == 1:     # Create and populate a database
            create = populate(type_option,create)
            continue
        
        if choice == 2:     # Retrieve records with a given key
            key_search(type_option,create)
            continue
        
        if choice == 3:     # Retrieve records with a given data
            data_search(type_option,create)
            continue        


        if choice == 4:     # Retrieve records with a given range of key values
            range_search(type_option,create)
            continue        
        
        if choice == 5:     # Destroy the database
            destroy()
            continue   
        
        if choice == 0:     # Quit 
            destroy()
            break        

    print ("Thanks for using!")
    tmp = input("Press Enter to End...")



if __name__ == "__main__":
    main(sys.argv[0:])
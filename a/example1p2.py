import bsddb
# Creatig a database
DATABASE = 'cstudents.db'
# Making it with BTree organization
db = bsddb.btopen(DATABASE,'c')
# Insertint a record
Sid = '123'
Name = 'James'
db[Sid] = Name
# Deleting a record
#Sid='123'
#del db[Sid]
#db.sync()
#Obtaining the result for a query
Sid = '123'
if (db.has_key(Sid)==True):
        sname = db[Sid]
        print(sname)
# Closing the connection
db.close()



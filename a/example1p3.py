#Create the database:
from bsddb3 import db
DATABASE = 'fruits.db'
database = db.DB()
database.open(DATABASE,None, db.DB_HASH, db.DB_CREATE) 

# Create a cursor
curs = database.cursor() 

# Insert records into the database:
## Using Cursors
#curs.put(b'apple', "red", db.DB_KEYFIRST)

# insertion using the database object’s put method
#database.put(b'pear', "green")

# Delete what the cursor point to
curs.first()
curs.delete()

# remove by using database object 
#database.delete(b'pear') 

# Display all data inside database
iter = curs.first()
while iter: 
	print(iter) 
	iter = curs.next()

## using the database object’s get method: only retrieves the value
result = database.get(b'pear')
print(result) 

# Close database and cursor
curs.close()
database.close() 

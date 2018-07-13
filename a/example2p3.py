from bsddb3 import db
DATABASE = 'fruits.db'
database = db.DB() 
# declare duplicates allowed before you create the database
database.set_flags(db.DB_DUP)
database.open(DATABASE,None, db.DB_HASH, db.DB_CREATE)
cur = database.cursor() 
# insert duplicates
cur.put(b'blue', "berry",db.DB_KEYFIRST)
cur.put(b'blue', "lemon",db.DB_KEYFIRST)
it = cur.first()
# prints no. of rows that have the same key as the key of the row cursor is pointing to
print(cur.count())
print(it)
# prints the next key-data pair if it is a duplicate
print(cur.next_dup()) 


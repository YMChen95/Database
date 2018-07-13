import com.sleepycat.db.*;
public class example1{
public static void main(String[] args){
  try { 
       //database configuration

       DatabaseConfig dbConfig = new DatabaseConfig();
       dbConfig.setType(DatabaseType.BTREE);
       dbConfig.setAllowCreate(true);
   	dbConfig.setSortedDuplicates(true);
      //Create a database 

      Database std_db = new Database("students.db", null, dbConfig);
	OperationStatus oprStatus;
      //Inserting Data into a database

      DatabaseEntry key = new DatabaseEntry();
      DatabaseEntry data = new DatabaseEntry();

      //Other variables

      String id = "1";
	String name="Mohammed";
data.setData(name.getBytes());
 data.setSize(name.length()); 
key.setData(id.getBytes()); 
key.setSize(id.length());
oprStatus = std_db.put(null, key, data);
////////
id = "2";
name="Ahmed";
data.setData(name.getBytes());
 data.setSize(name.length()); 
key.setData(id.getBytes()); 
key.setSize(id.length());
oprStatus = std_db.put(null, key, data);
////////////////
id = "3";
name="Ibrahim";
data.setData(name.getBytes());
 data.setSize(name.length()); 
key.setData(id.getBytes()); 
key.setSize(id.length());
oprStatus = std_db.put(null, key, data);

///////////////////////////////////////////////////////////////////////////////////////////////
// delete a row
//id = "1";
//key.setData(id.getBytes());
//key.setSize(id.length());
//oprStatus = std_db.delete(null, key);
//////////////////////////////////////////////////////////////////////////////////////////////
// Retreaving data from database
id = "1";
key.setData(id.getBytes());
key.setSize(id.length());
 DatabaseEntry data2 = new DatabaseEntry();
oprStatus = std_db.get(null, key, data2, LockMode.DEFAULT);
String b = new String (data2.getData());  // Converts from byte to string
System.out.println("Name = " + b + "\n");
//////////////////////////////////////////////////////////////////////////////////////////////
// Closing the connection
    std_db.close();

  } // end of try 

  catch (Exception ex) 
   { ex.getMessage();} 

}}


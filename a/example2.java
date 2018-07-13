import com.sleepycat.db.*;
public class example2{
public static void main(String[] args){
  try { 
OperationStatus oprStatus;
 DatabaseConfig dbConfig = new DatabaseConfig();
dbConfig.setType(DatabaseType.BTREE);
dbConfig.setAllowCreate(true);
Database std_db = new Database("students.db", null, dbConfig);
Cursor std_cursor = std_db.openCursor(null, null); // Create new cursor object
DatabaseEntry key = new DatabaseEntry();
DatabaseEntry data = new DatabaseEntry();
String searchkey = "1";
key.setData(searchkey.getBytes()); 
key.setSize(searchkey.length());
oprStatus = std_cursor.getSearchKey(key, data, LockMode.DEFAULT); // Returns OperationStatus
while (oprStatus == OperationStatus.SUCCESS)
{
String s = new String(data.getData( ));
System.out.println(s);
oprStatus = std_cursor.getNextDup(key, data, LockMode.DEFAULT);
// get next duplicate
}
   } // end of try 
  catch (Exception ex) 
   { ex.getMessage();} 
}}


import hashlib
import MySQLdb as db
from getpass import getpass


connection = db.connect(
  host='localhost',
  user='root',
  password = getpass(),
  database='simpleboundb',
  auth_plugin='mysql_native_password'
)

cursor= connection.cursor()

#cursor.execute('INSERT INTO Users VALUES ("deneme ins","Boran", "Kuzum", "blabla@gmail.com", "pasaport", "MATH");')

#cursor.execute(f'INSERT INTO Users VALUES ("hash ins","Taner", "Tolga", "blaasdfbla@gmail.com", "{hashlib.sha256("pasaport".encode()).hexdigest()}", "MATH");')

#cursor.execute('ALTER TABLE users MODIFY COLUMN password VARCHAR(256);')

#cursor.execute('INSERT INTO Database_Manager VALUES("furkan5", "password");')

connection.commit()

""" str = "GeeksforGeeks"
  
# encoding GeeksforGeeks using encode()
# then sending to SHA256()
result = hashlib.sha256(str.encode())
  
# printing the equivalent hexadecimal value.
print("The hexadecimal equivalent of SHA256 is : ")
print(result.hexdigest()) """



#print(hashlib.sha256("pasaport".encode()).hexdigest())





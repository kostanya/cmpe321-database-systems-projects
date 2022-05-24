import MySQLdb as db
from getpass import getpass


connection = db.connect(
  host='localhost',
  user='root',
  password = 'erk123H',
  database='simpleboundb',
  auth_plugin='mysql_native_password'
)

#cursor=connection.cursor()

#cursor.connect('')

#connection.commit()






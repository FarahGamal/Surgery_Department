import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Fofo-gamal153"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE SurgeryDepartment")
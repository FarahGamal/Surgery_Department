import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Fofo-gamal153",  #!change the password
  database= "SurgeryDepartment"
)

mycursor = mydb.cursor()

#? create database
#mycursor.execute("CREATE DATABASE SurgeryDepartment")
#? create rooms table
#mycursor.execute("CREATE TABLE Rooms (r_number VARCHAR(255) NOT NULL PRIMARY KEY, r_location INT)")
#? create equipment table
#mycursor.execute("CREATE TABLE Equipment (biocode VARCHAR(255) NOT NULL PRIMARY KEY, serial_number VARCHAR(255) NOT NULL, type VARCHAR(255) NOT NULL, r_check_up VARCHAR(255) NOT NULL, fk_r_no VARCHAR(255), FOREIGN KEY (fk_r_no) REFERENCES rooms (r_number))")
#? create Surgeries
#! fadal l foreign key pssn
#mycursor.execute("CREATE TABLE Surgeries (surgery_number VARCHAR(255) NOT NULL PRIMARY KEY, type VARCHAR(255) NOT NULL, start_time VARCHAR(255) NOT NULL, end_time VARCHAR(255) NOT NULL, r_no VARCHAR(255) NOT NULL, FOREIGN KEY (r_no) REFERENCES rooms (r_number))")

#!!!! FADAL L REPAIR TABLE WAITTING FOR TECHNICIANS TABLE

#? insert room numbes in room table
'''
sql=(" INSERT INTO Rooms (r_number) VALUES (%s) ")
val={
  '2',
  '3',
  '4',
  '5'
 }
mycursor.executemany(sql,val)
mydb.commit()
'''
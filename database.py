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
#! fadal l foreign key pssn mn table l patient
#mycursor.execute("CREATE TABLE Surgeries (surgery_number VARCHAR(255) NOT NULL PRIMARY KEY, type VARCHAR(255) NOT NULL, start_time VARCHAR(255) NOT NULL, end_time VARCHAR(255) NOT NULL, r_no VARCHAR(255) NOT NULL, FOREIGN KEY (r_no) REFERENCES rooms (r_number))")
#? create Managerial employees table
#mycursor.execute("CREATE TABLE Managerial_employees (SSN VARCHAR(255) NOT NULL UNIQUE,fname VARCHAR(250) NOT NULL,minit VARCHAR(250) NOT NULL,lname VARCHAR(250) NOT NULL,Phone_number VARCHAR(255) NOT NULL,Email VARCHAR(250),Gender VARCHAR(250) NOT NULL,Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL,Qualifications VARCHAR(250) NOT NULL,Address VARCHAR(250),ESSSN VARCHAR(255) NOT NULL,PRIMARY KEY (SSN),FOREIGN KEY (ESSSN) REFERENCES Managerial_employees(SSN))")
#? create Technicians table
#mycursor.execute("CREATE TABLE Technicians (SSN VARCHAR(255) NOT NULL UNIQUE,fname VARCHAR(250) NOT NULL,minit VARCHAR(250) NOT NULL,lname VARCHAR(250) NOT NULL,Phone_number int NOT NULL,Email VARCHAR(250),Gender VARCHAR(250) NOT NULL,Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL,Qualifications VARCHAR(250) NOT NULL,Address VARCHAR(250),TSSSN VARCHAR(255) NOT NULL,ESSN VARCHAR(255) NOT NULL,PRIMARY KEY (SSN),FOREIGN KEY (TSSSN) REFERENCES Technicians(SSN),FOREIGN KEY (ESSN) REFERENCES Managerial_employees(SSN))")
#? works on table
#mycursor.execute("CREATE TABLE Works_on (MSSN VARCHAR(255) NOT NULL,Sno VARCHAR(255) NOT NULL,FOREIGN KEY (MSSN) REFERENCES Managerial_employees (SSN), FOREIGN KEY (Sno) REFERENCES Surgeries (surgery_number))")
#!!!! FADAL L REPAIR TABLE WAITTING FOR TECHNICIANS TABLE
#mycursor.execute("CREATE TABLE Repair (tssn VARCHAR(255) NOT NULL, biocode VARCHAR(255) NOT NULL, FOREIGN KEY (tssn) REFERENCES Technicians (SSN), FOREIGN KEY (biocode) REFERENCES Equipment (biocode) )")
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


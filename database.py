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
#mycursor.execute("CREATE TABLE Equipment (biocode VARCHAR(255) NOT NULL PRIMARY KEY, serial_number VARCHAR(255) NOT NULL, \
#                      type VARCHAR(255) NOT NULL, r_check_up VARCHAR(255) NOT NULL, fk_r_no VARCHAR(255), FOREIGN KEY (fk_r_no) REFERENCES rooms (r_number))")
#? create Surgeries
#mycursor.execute("CREATE TABLE Surgeries (surgery_number VARCHAR(255) PRIMARY KEY, type VARCHAR(255) NOT NULL,\
 #                   start_time VARCHAR(255) NOT NULL, end_time VARCHAR(255) NOT NULL, code VARCHAR(255) ,r_no VARCHAR(255) ,\
  #                  pssn VARCHAR(255), FOREIGN KEY (pssn) REFERENCES Patient (pssn),FOREIGN KEY (r_no) REFERENCES rooms (r_number))")
#? create Managerial employees table
#mycursor.execute("CREATE TABLE Managerial_employees (essn VARCHAR(255)  PRIMARY KEY ,fname VARCHAR(250) NOT NULL\
#,Phone_number VARCHAR(255) NOT NULL,Email VARCHAR(250),Gender VARCHAR(250),Salary VARCHAR(255) ,\
# Position VARCHAR(250),Address VARCHAR(250) , esssn VARCHAR(255), FOREIGN KEY (esssn) REFERENCES Managerial_employees (essn))")
#? create Technicians table
#mycursor.execute("CREATE TABLE Technicians (ssn VARCHAR(255) PRIMARY KEY ,fname VARCHAR(250) NOT NULL\
 # ,Phone_number VARCHAR(255) NOT NULL,Email VARCHAR(250),Gender VARCHAR(250) NOT NULL,Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL,\
 #Qualifications VARCHAR(250) NOT NULL,Address VARCHAR(250), tssn VARCHAR(255) , tessn VARCHAR(255), \
  # FOREIGN KEY (tssn) REFERENCES Technicians(ssn),FOREIGN KEY (tessn) REFERENCES Managerial_employees(essn) )")
#? works on table  
#mycursor.execute("CREATE TABLE Works_on (sssn VARCHAR(255) NOT NULL,Sno VARCHAR(255) NOT NULL,\
 #FOREIGN KEY (sssn) REFERENCES Medical_stuff (mssn),\
  #FOREIGN KEY (Sno) REFERENCES Surgeries (surgery_number))")
#? repair table

#mycursor.execute("CREATE TABLE Repair (rssn VARCHAR(255) NOT NULL, biocode VARCHAR(255) NOT NULL, FOREIGN KEY (rssn) REFERENCES Technicians (ssn),\
 #FOREIGN KEY (biocode) REFERENCES Equipment (biocode) )")
#? Medical stuff table
#mycursor.execute( "CREATE TABLE Medical_stuff(mssn VARCHAR(255)   PRIMARY KEY,ID VARCHAR(255) NOT NULL ,fname VARCHAR(250) NOT NULL,\
#Phone_number VARCHAR(255) NOT NULL,Email VARCHAR(250)NOT NULL,Gender VARCHAR(250) NOT NULL,\
 #Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL, Address VARCHAR(250)NOT NULL,msssn VARCHAR(255) NOT NULL,\
 #FOREIGN KEY (msssn) REFERENCES Medical_stuff(mssn))")

#? Patient table
#mycursor.execute("CREATE TABLE Patient (pssn VARCHAR(255) ,ID VARCHAR(255) , fname VARCHAR(255), \
 #  Phone_number VARCHAR(255)   , Gender VARCHAR(255) , Email VARCHAR(255), Address VARCHAR(255), Insurance VARCHAR(255), \
  #   epssn VARCHAR(255) , mpssn VARCHAR(255), rno VARCHAR(255) , PRIMARY KEY(pssn), \
   #   FOREIGN KEY (epssn) REFERENCES Managerial_employees (essn), FOREIGN KEY (mpssn) REFERENCES Medical_stuff (mssn), \
    #    FOREIGN KEY (rno) REFERENCES Rooms(r_number))")

#?contact us form
#mycursor.execute("CREATE TABLE contact_us (fname VARCHAR(255), phone_number VARCHAR(255) PRIMARY KEY, subject VARCHAR(255))")   

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
'''
sql=(" INSERT INTO Managerial_employees (essn,fname,Phone_number,Email,Gender,Salary,Position,Address,esssn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
val={
  '1','omar','0111','omar@jbdgufdsh','male','10000000','doctor','AHAHAHAH','1',
  '2','omar','0111','omar@jbdgufdsh','male','10000000','doctor','AHAHAHAH','1'
 }
mycursor.executemany(sql,val)
mydb.commit()
'''

#mycursor.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, name VARCHAR(50), username VARCHAR(50), password VARCHAR(300), type VARCHAR(255))")

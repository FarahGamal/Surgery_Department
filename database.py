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
#mycursor.execute("CREATE TABLE Surgeries (surgery_number INT AUTO_INCREMENT PRIMARY KEY , type VARCHAR(255) NOT NULL,\
 #                   start_time VARCHAR(255) NOT NULL, end_time VARCHAR(255) NOT NULL, code VARCHAR(255) ,r_no VARCHAR(255) ,\
  #               pssn VARCHAR(255), FOREIGN KEY (pssn) REFERENCES Patient (pssn),FOREIGN KEY (r_no) REFERENCES rooms (r_number))")
#? create Managerial employees table
#mycursor.execute("CREATE TABLE Managerial_employees (essn VARCHAR(255)  PRIMARY KEY ,fname VARCHAR(250) NOT NULL\
#,Phone_number VARCHAR(255) NOT NULL,Gender VARCHAR(250),Salary VARCHAR(255) ,\
# Position VARCHAR(250),Address VARCHAR(250) , esssn VARCHAR(255), FOREIGN KEY (esssn) REFERENCES Managerial_employees (essn))")
#? create Technicians table
#mycursor.execute("CREATE TABLE Technicians (ssn VARCHAR(255) PRIMARY KEY ,fname VARCHAR(250) NOT NULL\
 # ,Phone_number VARCHAR(255) NOT NULL,Gender VARCHAR(250) NOT NULL,Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL,\
 # Address VARCHAR(250), tssn VARCHAR(255) , tessn VARCHAR(255), \
  # FOREIGN KEY (tssn) REFERENCES Technicians(ssn),FOREIGN KEY (tessn) REFERENCES Managerial_employees(essn) )")
#? works on table  
#mycursor.execute("CREATE TABLE Works_on (sssn VARCHAR(255) NOT NULL,Sno INT NOT NULL,\
 #FOREIGN KEY (sssn) REFERENCES Medical_stuff (mssn),\
  #FOREIGN KEY (Sno) REFERENCES Surgeries (surgery_number))")
#? repair table

#mycursor.execute("CREATE TABLE Repair (rssn VARCHAR(255) NOT NULL, biocode VARCHAR(255) NOT NULL, FOREIGN KEY (rssn) REFERENCES Technicians (ssn),\
 #FOREIGN KEY (biocode) REFERENCES Equipment (biocode) )")
#? Medical stuff table
#mycursor.execute( "CREATE TABLE Medical_stuff(mssn VARCHAR(255)   PRIMARY KEY,fname VARCHAR(250) NOT NULL,\
#Phone_number VARCHAR(255) NOT NULL,Gender VARCHAR(250) NOT NULL,\
 #Salary VARCHAR(255) NOT NULL,Position VARCHAR(250) NOT NULL, Address VARCHAR(250)NOT NULL,msssn VARCHAR(255),essn VARCHAR(255) ,\
 #FOREIGN KEY (msssn) REFERENCES Medical_stuff(mssn), FOREIGN KEY (essn) REFERENCES  Managerial_employees(essn))")

#? Patient table
#mycursor.execute("CREATE TABLE Patient (pssn VARCHAR(255)  , fname VARCHAR(255), \
 #  Phone_number VARCHAR(255)   , Gender VARCHAR(255) , Address VARCHAR(255), Insurance VARCHAR(255), \
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
sql=(" INSERT INTO Managerial_employees (essn,fname,Phone_number,Gender,Salary,Position,Address) VALUES (%s,%s,%s,%s,%s,%s,%s) ")
val={
  ('4321','omar','0111','male','10000000','admin','AHAHAHAH'),
  ('8888','ahmed','0111','male','10000000','admin','AHAHAHAH')
 }
mycursor.executemany(sql,val)
mydb.commit()
'''

#mycursor.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, name VARCHAR(50), username VARCHAR(50), password VARCHAR(300), ssn VARCHAR(255))")
'''
sql=("INSERT INTO medical_stuff(mssn,fname,Phone_number,Gender,Salary,Position,Address,essn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
val={
('1234','amr','01111111111','male','5000','doctor','19xxxx','4321'),
('5678','adel','01111111111','male','5000','nurse','19xxxx','4321')
}
mycursor.executemany(sql,val)
mydb.commit()
'''
'''
sql=("INSERT INTO Patient(pssn,fname,Phone_number,Gender,Address,Insurance,epssn,mpssn,rno) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
val={
('9876','mohamed','01111111111','male','19xxxx','yes','4321','1234','1'),
('5432','omar','01111111111','male','19xxxx','yes','8888','5678','2')
}
mycursor.executemany(sql,val)
mydb.commit()
'''
'''
sql=("INSERT INTO Technicians(ssn,fname,Phone_number,Gender,Salary,Position,Address,tessn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
val={
('5555','mohamed','01111111111','male','5000','biomedical','19xxxx','4321'),
('6666','omar','01111111111','male','5000','head biomedical','19xxxx','8888')
}
mycursor.executemany(sql,val)
mydb.commit()
'''
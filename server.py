import mysql.connector
from flask import Flask, redirect, url_for, request,render_template

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Fofo-gamal153",     #! change the password
  database="SurgeryDepartment"
)
mycursor = mydb.cursor()
app = Flask(__name__)

@app.route('/')
def hello_name():
   return render_template('index.html')

#!Eqipment add & view

@app.route('/add_equipment',methods = ['POST', 'GET'])
def addequipment():
   if request.method == 'POST': ##check if there is post data
      biocode = request.form['biocode']
      serial_number = request.form['serial_number']
      type = request.form['type']
      r_check_up = request.form['r_check_up']
      fk_r_no = request.form['fk_r_no']
      #print(name,department)
      sql = "INSERT INTO Equipment (biocode,serial_number,type,r_check_up, fk_r_no) VALUES (%s, %s, %s, %s, %s)"
      val = (biocode,serial_number, type, r_check_up, fk_r_no)
      mycursor.execute(sql, val)
      mydb.commit()   
      return render_template('index.html')
   else:
      return render_template('add_equipment.html')
      

@app.route('/view_equipment',methods = ['POST', 'GET'])
def viewequipment():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Equipment")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view_equipment.html',data=data)

#! Surgeries add & view

@app.route('/add_surgeries',methods = ['POST', 'GET'])
def addsurgeries():
   if request.method == 'POST': ##check if there is post data
      surgery_number = request.form['surgery_number']
      type = request.form['type']
      start_time = request.form['start_time']      
      end_time = request.form['end_time']
      r_no = request.form['r_no']      
      #print(name,department)
      sql = "INSERT INTO Surgeries (surgery_number,type, start_time, end_time, r_no) VALUES (%s, %s, %s, %s, %s)"
      val = (surgery_number, type, start_time, end_time, r_no)
      mycursor.execute(sql, val)
      mydb.commit()   
      return render_template('index.html')
   else:
      return render_template('add_surgeries.html')


@app.route('/view_surgeries',methods = ['POST', 'GET'])
def viewsurgeries():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Surgeries")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view_surgeries.html',data=data)


#! Rooms view

@app.route('/view_room',methods = ['POST', 'GET'])
def viewroom():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Rooms")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view_room.html',data=data)
      

#! Managerial Employees add & view

@app.route('/add_ManagerialEmployees',methods = ['POST', 'GET'])
def addManagerialEmployees():
    if request.method == 'POST': ##check if there is post data
     ssn = request.form['SSN']
     fname = request.form['fname']
     minit = request.form[' minit']
     lname = request.form['lname']
     Phone_number = request.form['Phone_number']
     Email = request.form['Email']
     Gender = request.form['Gender']
     Salary = request.form['Salary']
     Position = request.form['Position']
     Qualifications = request.form['Qualifications']
     Address = request.form['Address']
     esssn = request.form['ESSSN']
     #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,ESSSN)
     sql = "INSERT INTO Managerial_employees (SSN,fname,minit,lname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,ESSSN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     val = (ssn,fname,minit,lname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,esssn)
     mycursor.execute(sql, val)
     mydb.commit()
     return render_template('index.html')
    else: 
      return render_template ("add_ManagerialEmployees.html")

@app.route('/view_ManagerialEmployees',methods = ['POST', 'GET'])
def viewManagerialEmployees():
     if request.method == 'POST':
      return render_template('index.html')
     else:
      mycursor.execute("SELECT * FROM Managerial_employees")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('view_ManagerialEmployees.html',data=data)


#! Technicians add & view

@app.route('/add_Technicians')
def addTechnicians():
    if request.method == 'POST': ##check if there is post data
     SSN = request.form['SSN']
     fname = request.form['fname']
     minit = request.form[' minit']
     lname = request.form['lname']
     Phone_number = request.form['Phone_number']
     Email = request.form['Email']
     Gender = request.form['Gender']
     Salary = request.form['Salary']
     Position = request.form['Position']
     Qualifications = request.form['Qualifications']
     Address = request.form['Address']
     TSSSN = request.form['TSSSN']
     ESSN = request.form['ESSN']
     #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
     sql = "INSERT INTO Technicians (SSN,fname,minit,lname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     val = (SSN,fname,minit,lname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
     mycursor.execute(sql, val)
     mydb.commit()
     return render_template('index.html')
    else: 
      return render_template ("add_Technicians.html")

@app.route('/view_Technicians',methods = ['POST', 'GET'])
def viewTechnicians():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Technicians")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('view_Technicians.html',data=data)

#! Works on view

@app.route('/view_WorksOn',methods = ['POST', 'GET'])
def viewWorksOn():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Works_on")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('view_WorksOn.html',data=data)


if __name__ == '__main__':
   app.run()

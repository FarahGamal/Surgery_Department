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
      code = request.form['code'] 
      r_no = request.form['r_no']
      pssn = request.form['pssn']       
      #print(name,department)
      sql = "INSERT INTO Surgeries (surgery_number,type, start_time, end_time,code, r_no,pssn) VALUES (%s,%s,%s, %s, %s, %s, %s)"
      val = (surgery_number, type, start_time, end_time, code,r_no,pssn)
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
      essn = request.form['essn']
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Email = request.form['Email']
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Address = request.form['Address']
      esssn = request.form['esssn']
      #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
      sql = "INSERT INTO Managerial_employees (essn,fname,Phone_number,Email,Gender,Salary,Position,Address,esssn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (essn,fname,Phone_number,Email,Gender,Salary,Position,Address,esssn)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
    else: 
      return render_template ('add_ManagerialEmployees.html')



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

@app.route('/add_Technicians',methods = ['POST', 'GET'])
def addTechnicians():
    if request.method == 'POST': ##check if there is post data
      ssn = request.form['ssn']
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Email = request.form['Email']
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Qualifications = request.form['Qualifications']
      Address = request.form['Address']
      tssn = request.form['tssn']
      tessn = request.form['tessn']
      #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
      sql = "INSERT INTO Technicians (ssn,fname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,tssn,tessn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (ssn,fname,Phone_number,Email,Gender,Salary,Position,Qualifications,Address,tssn,tessn)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
    else: 
      return render_template ('add_Technicians.html')

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

#! Medical stuff add & view

@app.route('/AddMedicalStuff',methods = ['POST', 'GET'])
def addMedicalStuff():
    if request.method == 'POST': ##check if there is post data
      mssn = request.form['mssn']
      ID = request.form['ID']
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Email = request.form['Email']
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Address = request.form['Address']
      msssn = request.form['msssn']
     # esssn = request.form['essn']
      #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
      sql = "INSERT INTO Medical_stuff (mssn,ID,fname,Phone_number,Email,Gender,Salary,Position,Address,msssn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (mssn,ID,fname,Phone_number,Email,Gender,Salary,Position,Address,msssn)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
    else: 
      return render_template ('AddMedicalStuff.html')

@app.route('/ViewMedicalStuff',methods = ['POST', 'GET'])
def viewMedicalStuff():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Medical_stuff")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('ViewMedicalStuff.html',data=data)

#! Patient add & view

@app.route('/AddPatient',methods = ['POST', 'GET'])
def addPatient():
    if request.method == 'POST': ##check if there is post data
      pssn = request.form['pssn']
      ID = request.form['ID']
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Gender = request.form['Gender']
      Email = request.form['Email']
      Address = request.form['Address']
      Insurance = request.form['Insurance']
      epssn = request.form['epssn']
      mpssn = request.form['mpssn']
      rno = request.form['rno']
      #print(SSN,fname, minit,lname,Phone_number,Email, Gender,Salary,Position,Qualifications,Address,TSSSN,ESSN)
      sql = "INSERT INTO Patient (pssn,ID,fname,Phone_number,Gender,Email,Address,Insurance,epssn,mpssn,rno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (pssn,ID,fname,Phone_number,Gender,Email,Address,Insurance,epssn,mpssn,rno)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
    else: 
      return render_template ('AddPatient.html')


@app.route('/ViewPatient',methods = ['POST', 'GET'])
def viewPatient():
    if request.method == 'POST':
      return render_template('index.html')
    else:
        mycursor.execute("SELECT p.pssn,p.ID,p.fname,p.Phone_number,p.Gender,p.Email,p.Address,p.Insurance,d.fname,p.mpssn,p.rno \
           FROM Patient AS p JOIN Medical_stuff AS d ON p.mpssn=d.mssn")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
          }
        return render_template('ViewPatient.html',data=data)

#! repair add & view

@app.route('/addRepair',methods = ['POST', 'GET'])
def addRepair():
   if request.method == 'POST': ##check if there is post data
      rssn = request.form['rssn']
      biocode = request.form['biocode']
      #print(name,department)
      sql = "INSERT INTO Repair (rssn,biocode) VALUES ( %s, %s)"
      val = (rssn,biocode)
      mycursor.execute(sql, val)
      mydb.commit()   
      return render_template('index.html')
   else:
      return render_template('addRepair.html')

@app.route('/viewRepair',methods = ['POST', 'GET'])
def viewRepair():
    if request.method == 'POST':
      return render_template('index.html')
    else:
        mycursor.execute("SELECT fname,tssn,type,r.biocode \
          FROM Technicians AS t JOIN Repair as r ON t.tssn=r.rssn \
            JOIN Equipment AS e on r.biocode=e.biocode")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
          }
        return render_template('viewRepair.html',data=data)

if __name__ == '__main__':
   app.run()

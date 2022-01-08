import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, logging, flash
from flask_mysqldb import MySQL,MySQLdb 
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
import bcrypt

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

@app.route('/doctor')
def doctor():
   return render_template('doctor.html')

@app.route('/admin')
def admin():
   return render_template('admin.html')

@app.route('/patient',methods = ['POST', 'GET'])
def patient():
  if request.method =='POST':
    ssn=request.form.get('ssn')

    mycursor.execute("SELECT * FROM Patient WHERE pssn=%s",(ssn,))
    
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    p_ssn=mycursor.fetchall()
    print(p_ssn)
    data={
      'message':"data retrieved",
      'rec':p_ssn,
      'header':row_headers
    }
    return render_template('ViewPatient.html',data=data)
  return render_template('patient.html')

@app.route('/calendar')
def calendar():
   return render_template('calendar.html')

#!Eqipment add & view

@app.route('/add_equipment',methods = ['POST', 'GET'])
def addequipment():
   if request.method == 'POST': ##check if there is post data
      biocode = request.form['biocode']
      serial_number = request.form['serial_number']
      type = request.form['type']
      r_check_up = request.form['r_check_up']
      fk_r_no = request.form['fk_r_no']

      mycursor.execute("SELECT biocode FROM Equipment WHERE biocode=%s",(biocode,))
      check=mycursor.fetchone()

      mycursor.execute("SELECT r_number FROM rooms WHERE r_number=%s",(fk_r_no,))
      room=mycursor.fetchone()

      if check:
        flash("This Equipment already exist!","error")
        return render_template("add_equipment.html")
      elif room is None:
        flash("This Room does not  exist!","error")
        return render_template("add_equipment.html")
      else:
        sql = "INSERT INTO Equipment (biocode,serial_number,type,r_check_up, fk_r_no) VALUES (%s, %s, %s, %s, %s)"
        val = (biocode,serial_number, type, r_check_up, fk_r_no)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("This Equipment added successfully","done")    
        return render_template('add_equipment.html')
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
      type = request.form['type']
      start_time = request.form['start_time']      
      end_time = request.form['end_time']
      code = request.form['code'] 
      r_no = request.form['r_no']
      pssn = request.form['pssn']  

      mycursor.execute("SELECT r_number FROM rooms WHERE r_number=%s",(r_no,))
      rnumber=mycursor.fetchone()

      mycursor.execute("SELECT pssn FROM Patient WHERE pssn=%s",(pssn,))
      patientssn=mycursor.fetchone()

      if rnumber is None:
        flash("This room number does not exist!","error")
        return render_template("add_surgeries.html")
      elif patientssn is None:
        flash("This patient does not exist!","error")
        return render_template("add_surgeries.html")
      else:
        sql = "INSERT INTO Surgeries (type, start_time, end_time,code, r_no,pssn) VALUES (%s,%s, %s, %s, %s, %s)"
        val = ( type, start_time, end_time, code,r_no,pssn)
        mycursor.execute(sql, val)
        mydb.commit()   
        flash("This Surgery added successfully","done") 
        return render_template('add_surgeries.html')
   else:
      return render_template('add_surgeries.html')

@app.route('/view_surgeries',methods = ['POST', 'GET'])
def viewsurgeries():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT * FROM Surgeries  WHERE code IN ('red', 'yellow', 'green','blue') \
         ORDER BY CASE code \
           WHEN 'red' THEN 1 \
              WHEN 'yellow' THEN 2 \
                WHEN 'green' THEN 3 \
                  WHEN 'blue' THEN 4 \
                END , start_time ")
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
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Address = request.form['Address']
      esssn = request.form['esssn']

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(essn,))
      check=mycursor.fetchone()

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(esssn,))
      super=mycursor.fetchone()

      if check:
        flash("This Employee already exist!","error")
        return render_template("add_ManagerialEmployees.html")
      elif super is None:
        flash("This Supervisor does not exist!","error")
        return render_template("add_ManagerialEmployees.html")
      else:
        sql = "INSERT INTO Managerial_employees (essn,fname,Phone_number,Gender,Salary,Position,Address,esssn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (essn,fname,Phone_number,Gender,Salary,Position,Address,esssn)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("The Employee added successfully","done")
        return render_template('add_ManagerialEmployees.html')
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
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Address = request.form['Address']
      tssn = request.form['tssn']
      tessn = request.form['tessn']

      mycursor.execute("SELECT ssn FROM Technicians WHERE ssn=%s",(ssn,))
      check=mycursor.fetchone()

      mycursor.execute("SELECT ssn FROM Technicians WHERE ssn=%s",(tssn,))
      super=mycursor.fetchone()

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(tessn,))
      emp=mycursor.fetchone()

      if check:
        flash("This Technicians already exist!","error")
        return render_template("add_Technicians.html")
      elif super is None:
        flash("This Supervisor does not exist!","error")
        return render_template("add_Technicians.html")
      elif emp is None:
        flash("This Employee already exist!","error")
        return render_template("add_Technicians.html")
      else:
        sql = "INSERT INTO Technicians (ssn,fname,Phone_number,Gender,Salary,Position,Address,tssn,tessn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (ssn,fname,Phone_number,Gender,Salary,Position,Address,tssn,tessn)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("The Technicians added successfully","done")
        return render_template('add_Technicians.html')
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

@app.route('/add_WorksOn',methods = ['POST', 'GET'])
def addWorksOn():
    if request.method == 'POST': ##check if there is post data
      sssn = request.form['sssn']
      Sno = request.form['Sno']
      
      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(sssn,))
      med=mycursor.fetchone()

      mycursor.execute("SELECT surgery_number FROM Surgeries WHERE surgery_number=%s",(Sno,))
      snumber=mycursor.fetchone()

      if med is None:
        flash("This medical stuff not found!","error")
        return render_template("add_WorksOn.html")
      elif snumber is None:
        flash("This surgery number not found!","error")
        return render_template("add_WorksOn.html")
      else:
        sql = "INSERT INTO Works_on (sssn,Sno) VALUES (%s,%s)"
        val = (sssn,Sno)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("Successfully added","done")
        return render_template('add_WorksOn.html')
    else: 
      return render_template ('add_WorksOn.html')

@app.route('/view_WorksOn',methods = ['POST', 'GET'])
def viewWorksOn():
    if request.method == 'POST':
      return render_template('index.html')
    else:
      mycursor.execute("SELECT m.fname,s.type \
          FROM Works_on AS w JOIN Medical_stuff AS m ON m.mssn = w.sssn \
            JOIN Surgeries AS s ON w.Sno = s.surgery_number")
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
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Gender = request.form['Gender']
      Salary = request.form['Salary']
      Position = request.form['Position']
      Address = request.form['Address']
      msssn = request.form['msssn']
      essn = request.form['essn']

      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(mssn,))
      check=mycursor.fetchone()

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(essn,))
      emp=mycursor.fetchone()

      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(msssn,))
      super=mycursor.fetchone()

      if check:
        flash("This medical stuff  already exist!","error")
        return render_template("AddMedicalStuff.html")
      elif emp is None:
        flash("This Employee does not exist!","error")
        return render_template("AddMedicalStuff.html")
      elif super is None:
        flash("This Supervisor does not exist!","error")
        return render_template("AddMedicalStuff.html")
      else:
        sql = "INSERT INTO Medical_stuff (mssn,fname,Phone_number,Gender,Salary,Position,Address,msssn,essn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (mssn,fname,Phone_number,Gender,Salary,Position,Address,msssn,essn)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("The medical stuff added successfully","done")
        return render_template('AddMedicalStuff.html')
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
      fname = request.form['fname']
      Phone_number = request.form['Phone_number']
      Gender = request.form['Gender']
      Address = request.form['Address']
      Insurance = request.form['Insurance']
      epssn = request.form['epssn']
      mpssn = request.form['mpssn']
      rno = request.form['rno']

      mycursor.execute("SELECT pssn FROM Patient WHERE pssn=%s",(pssn,))
      check=mycursor.fetchone()

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(epssn,))
      emp=mycursor.fetchone()

      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(mpssn,))
      med=mycursor.fetchone()

      mycursor.execute("SELECT r_number FROM rooms WHERE r_number=%s",(rno,))
      room=mycursor.fetchone()

      if check:
        flash("This Patient already exist!","error")
        return render_template("AddPatient.html")
      elif emp is None:
        flash("This Employee does not exist!","error")
        return render_template("AddPatient.html")
      elif med is None:
        flash("This Doctor/Nurse does not exist!","error")
        return render_template("AddPatient.html")
      elif room is None:
        flash("This Room does not exist!","error")
        return render_template("AddPatient.html")
      else:
        sql = "INSERT INTO Patient (pssn,fname,Phone_number,Gender,Address,Insurance,epssn,mpssn,rno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (pssn,fname,Phone_number,Gender,Address,Insurance,epssn,mpssn,rno)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("The Patient added successfully","done")
        return render_template('AddPatient.html')
    else: 
      return render_template ('AddPatient.html')


@app.route('/ViewPatient',methods = ['POST', 'GET'])
def viewPatient():
    if request.method == 'POST':
      return render_template('index.html')
    else:
        mycursor.execute("SELECT p.pssn,p.ID,p.fname,p.Phone_number,p.Gender,p.Address,p.Insurance,d.fname,p.mpssn,p.rno \
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

      mycursor.execute("SELECT ssn FROM Technicians WHERE ssn=%s",(rssn,))
      tech=mycursor.fetchone()

      mycursor.execute("SELECT biocode FROM Equipment WHERE biocode=%s",(biocode,))
      equ=mycursor.fetchone()

      if tech is None:
        flash("The SSN of this technician not found!","error")
        return render_template("addRepair.html")
      elif equ is None:
        flash("This biocode not found!","error")
        return render_template("addRepair.html")
      else:
        sql = "INSERT INTO Repair (rssn,biocode) VALUES ( %s, %s)"
        val = (rssn,biocode)
        mycursor.execute(sql, val)
        mydb.commit()   
        flash("Successfully added","done")
        return render_template('addRepair.html')
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

#! contact us add & view

@app.route('/add_contact_us',methods = ['POST', 'GET'])
def addcontactus():
   if request.method == 'POST': ##check if there is post data
      fname = request.form['fname']
      phone_number = request.form['phone_number']
      subject = request.form['subject']
      #print(name,department)
      sql = "INSERT INTO contact_us (fname,phone_number,subject) VALUES ( %s,%s, %s)"
      val = (fname,phone_number,subject)
      mycursor.execute(sql, val)
      mydb.commit()   
      return render_template('index.html')
   else:
      return render_template('add_contact_us.html')

@app.route('/view_contact_us',methods = ['POST', 'GET'])
def viewContactus():
    if request.method == 'POST':
      return render_template('index.html')
    else:
        mycursor.execute("SELECT * FROM contact_us")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
          }
        return render_template('view_contact_us.html',data=data)
###############################################################################################################################!
@app.route("/register",methods=["GET","POST"])
def register():
  
  if request.method=="POST" :
    name=request.form.get("name")
    username=request.form.get("username")
    password=request.form.get("password")
    confirm=request.form.get("confirm")
    secure_password=sha256_crypt.encrypt(str(password))

    mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    account = mycursor.fetchone()
    if account:
      return render_template("register.html",error="THIS ACCOUNT ALREADY EXIST")
    elif password==confirm:
      sql = "INSERT INTO users (name,username,password) VALUES ( %s,%s, %s)"
      val = (name,username,secure_password)
      mycursor.execute(sql, val)
      mydb.commit()
      flash("you are registerd and can login", "success")
      return render_template("login.html",message="you are registerd and can login")
    else:
      flash("password does not match", "danger")
      return render_template("register.html",error="PASSWORD DOES NOT MATCH")

  return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
  if request.method=="POST":
    username=request.form.get("username")
    password=request.form.get("password")

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT username FROM users WHERE username=%s",(username,))
    usernamedata=mycursor.fetchone()

    mycursor.execute("SELECT password FROM users WHERE username=%s",(username,))
    passwordata=mycursor.fetchone()
    ##############
    mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(username,))
    mdata=mycursor.fetchone()
    print(mdata)

    mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",(username,))
    edata=mycursor.fetchone()
    print(edata)

    mycursor.execute("SELECT pssn FROM Patient WHERE pssn=%s",(username,))
    pdata=mycursor.fetchone()
    print(pdata)


    if usernamedata is None:
      flash("No username","danger")
      return render_template("login.html")
    else:
      for passwor_data in passwordata:
        if sha256_crypt.verify(password,passwor_data):
          session["log"]=True
          flash("You are now login","success")
          if mdata:
            mycursor.execute("SELECT * FROM Patient WHERE mpssn=%s",(username,))
            row_headers=[x[0] for x in mycursor.description] #this will extract row headers
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            data={
              'message':"data retrieved",
              'rec':myresult,
              'header':row_headers
            }
            return render_template("newdoctor.html",data=data)
          elif edata:
            mycursor.execute("SELECT fname FROM Managerial_employees WHERE essn=%s",(username,))
            name=mycursor.fetchone()
            print(name)
            return render_template("admin.html")
          elif pdata :
            mycursor.execute("SELECT * FROM Patient WHERE pssn=%s",(username,))
            row_headers=[x[0] for x in mycursor.description] #this will extract row headers
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            data={
              'message':"data retrieved",
              'rec':myresult,
              'header':row_headers
            }
            return render_template("newpatient.html",data=data)
          else:
            return render_template("newhome.html")
        else:
          flash("incorrect password","danger")
          return render_template("login.html",error="incorrect password")

  return render_template("login.html")

@app.route("/logout")
def logout():
  session.clear()
  flash("You are logger out","success")
  return render_template("index.html")


if __name__ == '__main__':
  app.secret_key="1234567dailywebcoding"
  app.run(debug=True)

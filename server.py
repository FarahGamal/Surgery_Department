from logging import error
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

@app.route('/calendar')
def calendar():
   return render_template('calendar.html')

#!Eqipment add & view
      
@app.route('/equipment',methods = ['POST', 'GET'])
def equipment():
    if request.method == 'POST':
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT biocode FROM Equipment WHERE biocode=%s",(ssn,))
      mm = mycursor.fetchall()
      if mm is None:
        return render_template('view_equipment.html')
      else:
        mycursor.execute("DELETE FROM Repair WHERE biocode=%s",(ssn,))
        mydb.commit()
        mycursor.execute("DELETE FROM Equipment WHERE biocode=%s",(ssn,))
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        mycursor.execute("SELECT biocode,type FROM Equipment")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        p_ssn=mycursor.fetchall()
        print(p_ssn)
        data={
          'message':"data retrieved",
          'rec':p_ssn,
          'header':row_headers
        }
        return render_template('view_equipment.html',data=data)
    else:
      mycursor.execute("SELECT biocode,type FROM Equipment")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('equipment.html',data=data)
    
###################################################################?
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
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT biocode,serial_number,type,r_check_up,fk_r_no FROM Equipment WHERE biocode=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('equipment.html',data=data)
    else:
      mycursor.execute("SELECT biocode,type FROM Equipment")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view_equipment.html',data=data)

#! Surgeries add & view

@app.route('/surgery',methods = ['POST', 'GET'])
def deletesurgeries():
    if request.method == 'POST':
      ssn=request.form.get('ssn')

      mycursor.execute("SELECT surgery_number FROM Surgeries WHERE surgery_number=%s",(ssn,))
      mm = mycursor.fetchall()
      print(mm)

      if mm is None:
        flash("This SSN does not exist!","error")
        return render_template('view_surgeries.html')
      else:
        mycursor.execute("DELETE FROM Works_On WHERE Sno=%s",(ssn,))
        mydb.commit()
        #############
        mycursor.execute("DELETE FROM Surgeries WHERE surgery_number=%s",(ssn,))
        mydb.commit()
        ##########
        mycursor.execute("SELECT surgery_number,type FROM Surgeries  WHERE code IN ('red', 'yellow', 'green','blue') \
         ORDER BY CASE code \
           WHEN 'red' THEN 1 \
              WHEN 'yellow' THEN 2 \
                WHEN 'green' THEN 3 \
                  WHEN 'blue' THEN 4 \
                END , start_time ")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        p_ssn=mycursor.fetchall()
        print(p_ssn)
        data={
          'message':"data retrieved",
          'rec':p_ssn,
          'header':row_headers
        }
        return render_template('view_surgeries.html',data=data)
    else:
      mycursor.execute("SELECT surgery_number,type FROM Surgeries  WHERE code IN ('red', 'yellow', 'green','blue') \
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
        sql = "INSERT INTO Surgeries (surgery_number,type, start_time, end_time,code, r_no,pssn) VALUES (%s,%s,%s, %s, %s, %s, %s)"
        val = (surgery_number, type, start_time, end_time, code,r_no,pssn)
        mycursor.execute(sql, val)
        mydb.commit()   
        flash("This Surgery added successfully","done") 
        return render_template('add_surgeries.html')
   else:
      return render_template('add_surgeries.html')

      
@app.route('/view_surgeries',methods = ['POST', 'GET'])
def viewsurgeries():
    if request.method == 'POST':
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT s.surgery_number,s.type,s.start_time,s.end_time,s.code,s.r_no,p.fname \
        FROM Surgeries AS s JOIN Patient AS p ON s.pssn=p.pssn WHERE s.surgery_number=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('surgery.html',data=data)
    else:
      mycursor.execute("SELECT surgery_number,type FROM Surgeries  WHERE code IN ('red', 'yellow', 'green','blue') \
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

@app.route('/emp',methods = ['POST', 'GET'])
def empoption():
  if request.method == 'POST':
    value=request.form.get('value')
    print(value)
    if value == 'receptionist':
        mycursor.execute("SELECT essn,fname,Position FROM Managerial_employees WHERE Position=%s",(value,))
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
        }
        return render_template('emp.html',data=data)
    elif value == 'assistant':
        mycursor.execute("SELECT essn,fname,Position FROM Managerial_employees WHERE Position=%s",(value,))
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
        }
        return render_template('emp.html',data=data)
    elif value == 'supervisor':
      mycursor.execute("SELECT s.essn,s.fname,s.Position FROM Managerial_employees AS f \
        JOIN Managerial_employees AS s ON f.essn=s.esssn")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
      }
      return render_template('emp.html',data=data)
    else:
      mycursor.execute("SELECT essn, fname, Position FROM Managerial_employees")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('ViewMedicalStuff.html',data=data)

@app.route('/employee',methods = ['POST', 'GET'])
def deletemployee():
     if request.method == 'POST':
        ssn=request.form.get('ssn')
        mycursor.execute("SELECT essn FROM Medical_stuff WHERE essn=%s",(ssn,))
        mm = mycursor.fetchall()
        print(mm)
        if mm is None:
          flash("This SSN does not exist!","error")
          return render_template('view_ManagerialEmployees.html')
        else:
          mycursor.execute("UPDATE Managerial_employees SET esssn=%s WHERE esssn=%s",(None,ssn,))
          mydb.commit()
          ##########################
          mycursor.execute("UPDATE Patient SET epssn=%s WHERE epssn=%s",(None,ssn,))
          mydb.commit()
          ############################
          mycursor.execute("DELETE FROM Medical_stuff WHERE essn=%s",(ssn,))
          mydb.commit()
          ###################
          mycursor.execute("UPDATE Technicians SET tessn=%s WHERE tessn=%s",(None,ssn,))
          mydb.commit()
          ###################
          mycursor.execute("DELETE FROM Managerial_employees WHERE essn=%s",(ssn,))
          mydb.commit()

          print(mycursor.rowcount, "record(s) deleted")
          mycursor.execute("SELECT essn, fname, Position FROM Managerial_employees")
          row_headers=[x[0] for x in mycursor.description] #this will extract row headers
          p_ssn=mycursor.fetchall()
          print(p_ssn)
          data={
            'message':"data retrieved",
            'rec':p_ssn,
            'header':row_headers
          }
          return render_template('view_ManagerialEmployees.html',data=data)
     else:
      mycursor.execute("SELECT essn, fname, Position FROM Managerial_employees")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('employee.html',data=data)

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
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT p.essn,p.fname,p.Phone_number,p.Gender,p.Salary,p.Position,p.Address,d.fname \
            FROM Managerial_employees AS p LEFT OUTER JOIN Managerial_employees AS d ON p.esssn = d.essn WHERE p.essn=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('employee.html',data=data)
     else:
      mycursor.execute("SELECT essn, fname, Position FROM Managerial_employees")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('view_ManagerialEmployees.html',data=data)


#! Technicians add & view
@app.route('/tech',methods = ['POST', 'GET'])
def technician():
  if request.method == 'POST':
    value=request.form.get('value')
    print(value)
    if value == 'Head biomedical':
        mycursor.execute("SELECT ssn,fname,Position FROM Technicians WHERE Position=%s",(value,))
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
        }
        return render_template('tech.html',data=data)
    elif value == 'biomedical':
        mycursor.execute("SELECT ssn,fname,Position FROM Technicians WHERE Position=%s",(value,))
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
        }
        return render_template('tech.html',data=data)
    elif value == 'supervisor':
      mycursor.execute("SELECT s.ssn,s.fname,s.Position FROM Technicians AS f \
        JOIN Technicians AS s ON f.ssn=s.tssn")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
      }
      return render_template('tech.html',data=data)
    else:
      mycursor.execute("SELECT ssn,fname,Position FROM Technicians")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('view_Technicians.html',data=data)


@app.route('/technician',methods = ['POST', 'GET'])
def deleteTechnicians():
    if request.method == 'POST':
      ssn=request.form.get('ssn')

      mycursor.execute("SELECT ssn FROM Technicians WHERE ssn=%s",(ssn,))
      mm = mycursor.fetchall()
      print(mm)
      
      if mm is None:
        flash("This SSN does not exist!","error")
        return render_template('view_Technicians.html')
      else:
        mycursor.execute("DELETE FROM Repair WHERE rssn=%s",(ssn,))
        mydb.commit()
        #############
        mycursor.execute("UPDATE Technicians SET tssn=%s WHERE tssn=%s",(None,ssn,))
        mydb.commit()
        ##############
        mycursor.execute("DELETE FROM Technicians WHERE ssn=%s",(ssn,))
        mydb.commit()
        ##########
        mycursor.execute("SELECT ssn,fname,Position FROM Technicians")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        p_ssn=mycursor.fetchall()
        print(p_ssn)
        data={
          'message':"data retrieved",
          'rec':p_ssn,
          'header':row_headers
        }
        return render_template('view_Technicians.html',data=data)
    else:
      mycursor.execute("SELECT ssn,fname,Position FROM Technicians")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('technician.html',data=data)

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
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT p.ssn,p.fname,p.Phone_number,p.Gender,p.Salary,p.Position,p.Address,d.fname \
            FROM Technicians AS p LEFT OUTER JOIN Technicians AS d ON p.tssn = d.ssn WHERE p.ssn=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('technician.html',data=data)
    else:
      mycursor.execute("SELECT ssn,fname,Position FROM Technicians")
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
@app.route('/doctor',methods = ['POST', 'GET'])
def deletedoctor():
    if request.method == 'POST':
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",(ssn,))
      mm = mycursor.fetchall()
      print(mm)
      if mm is None:
        flash("This SSN does not exist!","error")
        return render_template('ViewMedicalStuff.html')
      else:
        mycursor.execute("UPDATE Medical_stuff SET msssn=%s WHERE msssn=%s",(None,ssn,))
        mydb.commit()
        ##########################
        mycursor.execute("UPDATE Patient SET mpssn=%s WHERE mpssn=%s",(None,ssn,))
        mydb.commit()
        ############################
        mycursor.execute("DELETE FROM Works_on WHERE sssn=%s",(ssn,))
        mydb.commit()
        ############################
        mycursor.execute("DELETE FROM Medical_stuff WHERE mssn=%s",(ssn,))
        mydb.commit()
        ###################
        print(mycursor.rowcount, "record(s) deleted")
        mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        p_ssn=mycursor.fetchall()
        print(p_ssn)
        data={
          'message':"data retrieved",
          'rec':p_ssn,
          'header':row_headers
        }
        return render_template('ViewMedicalStuff.html',data=data)
    else:
      mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('doctor.html',data=data)

@app.route('/doctoroption',methods = ['POST', 'GET'])
def doctoroption():
  if request.method == 'POST':
    value=request.form.get('value')
    print(value)
    if value == 'doctor':
        mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff WHERE Position=%s",(value,))
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
        }
        return render_template('doctoroption.html',data=data)
    elif value== 'nurse':
      mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff WHERE Position=%s",(value,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
      }
      return render_template('doctoroption.html',data=data)
    elif value == 'supervisor':
      mycursor.execute("SELECT s.mssn,s.fname,s.Position FROM Medical_stuff AS f \
        JOIN Medical_stuff AS s ON f.mssn=s.msssn")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
      }
      return render_template('doctoroption.html',data=data)
    else:
      mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('ViewMedicalStuff.html',data=data)

#################################################################################?
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
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT p.mssn,p.fname,p.Phone_number,p.Gender,p.Salary,p.Position,p.Address,d.fname \
            FROM Medical_stuff AS p LEFT OUTER JOIN Medical_stuff AS d ON p.msssn = d.mssn WHERE p.mssn=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('doctor.html',data=data)
    else:
      mycursor.execute("SELECT mssn,fname,Position FROM Medical_stuff")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
        }
      return render_template('ViewMedicalStuff.html',data=data)

#! Patient add & view
@app.route('/patient',methods = ['POST', 'GET'])
def deletePatient():
    if request.method == 'POST':
        ssn=request.form.get('ssn')
        mycursor.execute("SELECT pssn FROM Patient WHERE pssn=%s",(ssn,))
        mm = mycursor.fetchall()
        print(mm)
        if mm is None:
          flash("This SSN does not exist!","error")
          return render_template('ViewPatient.html')
        else:
          mycursor.execute("SELECT surgery_number FROM Surgeries WHERE pssn=%s",(ssn,))
          sno=mycursor.fetchone()
          mycursor.execute("DELETE FROM Works_On WHERE Sno=%s" ,sno)
          mydb.commit()
          ####################
          mycursor.execute("DELETE FROM Surgeries WHERE pssn=%s",(ssn,))
          mydb.commit()
          ####################
          mycursor.execute("DELETE FROM Patient WHERE pssn=%s",(ssn,))
          mydb.commit()

          print(mycursor.rowcount, "record(s) deleted")
          mycursor.execute("SELECT pssn,fname,cond,rno \
           FROM Patient ")
          row_headers=[x[0] for x in mycursor.description] #this will extract row headers
          p_ssn=mycursor.fetchall()
          print(p_ssn)
          data={
            'message':"data retrieved",
            'rec':p_ssn,
            'header':row_headers
          }
          return render_template('ViewPatient.html',data=data)
    else:
        mycursor.execute("SELECT p.pssn,p.fname,p.Phone_number,p.Gender,p.Address,p.Insurance,p.cond,d.fname,p.rno \
           FROM Patient AS p JOIN Medical_stuff AS d ON p.mpssn=d.mssn ")
        row_headers=[x[0] for x in mycursor.description] #this will extract row headers
        myresult = mycursor.fetchall()
        data={
          'message':"data retrieved",
          'rec':myresult,
          'header':row_headers
          }
        return render_template('patient.html',data=data)


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
      cond = request.form['cond']

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
        sql = "INSERT INTO Patient (pssn,fname,Phone_number,Gender,Address,Insurance,epssn,mpssn,rno,cond) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (pssn,fname,Phone_number,Gender,Address,Insurance,epssn,mpssn,rno,cond)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("The Patient added successfully","done")
        return render_template('AddPatient.html')
    else: 
      return render_template ('AddPatient.html')


@app.route('/ViewPatient',methods = ['POST', 'GET'])
def viewPatient():
    if request.method == 'POST':
      ssn=request.form.get('ssn')
      mycursor.execute("SELECT p.pssn,p.fname,p.Phone_number,p.Gender,p.Address,p.Insurance,p.cond,d.fname,p.rno \
           FROM Patient AS p JOIN Medical_stuff AS d ON p.mpssn=d.mssn WHERE pssn=%s",(ssn,))
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      p_ssn=mycursor.fetchall()
      print(p_ssn)
      data={
        'message':"data retrieved",
        'rec':p_ssn,
        'header':row_headers
      }
      return render_template('patient.html',data=data)
    else:
        mycursor.execute("SELECT pssn,fname,cond,rno \
           FROM Patient ")
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
        mycursor.execute("SELECT fname,ssn,type,r.biocode \
          FROM Technicians AS t JOIN Repair as r ON t.ssn=r.rssn \
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
    ssn=request.form.get("ssn")
    secure_password=sha256_crypt.encrypt(str(password))

    mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    account = mycursor.fetchone()

    if account:
      return render_template("register.html" ,error="already exist")
    elif password==confirm:
      sql = "INSERT INTO users (name,username,password,ssn) VALUES (%s,%s,%s, %s)"
      val = (name,username,secure_password,ssn)
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
    userdata=mycursor.fetchone()

    mycursor.execute("SELECT password FROM users WHERE username=%s",(username,))
    passwordata=mycursor.fetchone()


    if userdata is None:
      flash("No username","danger")
      return render_template("login.html", error="NO USERNAME")
    else:
      mycursor.execute("SELECT ssn FROM users WHERE username=%s",(username,))
      ssn=mycursor.fetchone()
      print(ssn)
      ##############
      mycursor.execute("SELECT mssn FROM Medical_stuff WHERE mssn=%s",ssn)
      mdata=mycursor.fetchone()
      print(mdata)

      mycursor.execute("SELECT essn FROM Managerial_employees WHERE essn=%s",ssn)
      edata=mycursor.fetchone()
      print(edata)

      mycursor.execute("SELECT pssn FROM Patient WHERE pssn=%s",ssn)
      pdata=mycursor.fetchone()
      print(pdata)
      for passwor_data in passwordata:
        if sha256_crypt.verify(password,passwor_data):
          session["log"]=True
          #flash("You are now login","success")
          if mdata:
            mycursor.execute("SELECT p.pssn,p.fname,p.Phone_number,p.Gender,p.Address,p.Insurance,p.cond,d.fname,p.rno \
                  FROM Patient AS p JOIN Medical_stuff AS d ON p.mpssn=d.mssn WHERE mpssn=%s",ssn)
            row_headers=[x[0] for x in mycursor.description] #this will extract row headers
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            data={
              'message':"data retrieved",
              'rec':myresult,
              'header':row_headers
            }
            return render_template("newdoctor.html",data=data,message="Welcome," + username)
          elif edata:
              return render_template("admin.html",message=" " + username)
          elif pdata :
              mycursor.execute("SELECT p.pssn,p.fname,p.Phone_number,p.Gender,p.Address,p.Insurance,p.cond,d.fname,p.rno \
                  FROM Patient AS p JOIN Medical_stuff AS d ON p.mpssn=d.mssn WHERE pssn=%s",ssn)
              row_headers=[x[0] for x in mycursor.description] #this will extract row headers
              myresult = mycursor.fetchall()
              print(myresult)
              for x in myresult:
                  print(x)
              data={
                'message':"data retrieved",
                'rec':myresult,
                'header':row_headers
              }
              return render_template("newpatient.html",data=data,message="Welcome, " + username)
          else:
            return render_template("newhome.html")
        else:
          #flash("incorrect password","danger")
          return render_template("login.html",error="incorrect password")

  return render_template("login.html")

@app.route("/logout")
def logout():
  session.clear()
  #flash("You are logger out","success")
  return render_template("index.html")


if __name__ == '__main__':
  app.secret_key="1234567dailywebcoding"
  app.run(debug=True)

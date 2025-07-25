from flask import Flask, render_template, request , url_for
# import Mysql package
from flask_mysqldb import MySQL
from datetime import *

app = Flask(__name__)
# connect database
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'muhammad'
app.config['MYSQL_PASSWORD'] = '034971'
app.config['MYSQL_DB'] = 'flaskdb'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/trainer')
def trainer_details():
    return render_template('trainer_details.html')

@app.route('/trainer_create',methods=['POST','GET'])
def trainer_create():
    if request.method == 'POST':
        fname_data=request.form['fname']
        lname_data= request.form['lname']
        email_data = request.form['email']
        design_data = request.form['design']
        course_data=request.form['course']
        current_date = date.today()

        # store data into database --> tables 
        sql = 'INSERT INTO trainer_details (fname,lname,email,design,course,datetime) VALUES (%s,%s,%s,%s,%s,%s)'
        val = (fname_data,lname_data,email_data,design_data,course_data,current_date)

        # make connection
        cursor = mysql.connection.cursor()
        # execute sql query
        cursor.execute(sql,val)
        # commit
        mysql.connection.commit()
        #close database
        cursor.close()

        return 'Data has been successfully stored.'
    

if __name__ == '__main__':
    app.run(debug=True)










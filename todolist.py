from flask import Flask, render_template, url_for, request, redirect, session
from flask import flash,get_flashed_messages
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import secrets
#import register form class from another page 
from forms import RegisterForm,Loginform

# create app object
app = Flask(__name__)
# configure flask to database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='muhammad'
app.config['MYSQL_PASSWORD']='Shahzib123!'
app.config['MYSQL_DB']='todo'
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# secret key for session
app.secret_key = secrets.token_hex(16)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    form=RegisterForm()
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # send data to database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

           
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Loginform()   # flag to send to template

    if form.validate_on_submit():
        username = form.username.data.strip()    # .strip() to remove whitespaces
        password = form.password.data.strip()

         # store data               
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()    # (user) is basically a tuple not a dict, it saves data like (1,'Muhammad Hammaed','1234hsdflj')
        cursor.close()
        
        if user:
            stored_hash = user[2]
            if bcrypt.check_password_hash(stored_hash, password):
                session['username'] = user[1]   # column 1 is username --> [id, username,password]
                session['user_id'] = user[0]   # column 0 is id  -->  [id, username,password]
                return redirect(url_for('display_all'))
        
    return render_template('login.html',form=form)

# Logout
@app.route('/logout')
def logout():
    error = None
    # session.pop('username', None)
    session.clear()
    error = "You are logged out."
    # return redirect(url_for('login'),error=error)    # redirect to login
    return render_template('login.html', error= error)

@app.route('/display_all', methods=['GET'])
def display_all():
    # if the user didnt login dont show this route
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM add_task WHERE user_id = %s', (session['user_id'],))   
    all_data = cursor.fetchall()
    cursor.close()

    return render_template('diplay_data.html', mydata=all_data,)

@app.route('/task_to_add', methods=['POST'])
def task_to_add():
    error = None

    if 'username' not in session:
        return redirect(url_for('login'))
    # get task
    new_task = request.form['title'].strip()
    # get due date from the form
    due_date = request.form.get('due_date').strip()

    # handle if task is empty
    if new_task == '' or due_date == '':
        error = "Please fill the fields."
        return render_template('diplay_data.html',error = error)
    
    #else store task in database
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO add_task (title,due_date,user_id) VALUES (%s,%s,%s)', (new_task,due_date,session['user_id']))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))

@app.route('/remove_task', methods=['POST'])
def task_to_remove():
    if 'username' not in session:
        return redirect(url_for('login'))

    remove_title = request.form['remove_title']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM add_task WHERE user_id =%s AND id = %s', (session['user_id'],remove_title))
    
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))

@app.route('/mark_as_done', methods=['POST'])
def mark_as_done():
    if 'username' not in session:
        return redirect(url_for('login'))

    task_id = request.form['task_done']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE add_task SET is_done = 1 WHERE id = %s AND user_id = %s', (task_id,session['user_id']))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))


# edit task
@app.route('/edit/<int:id>', methods=["GET"])
def edit(id):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM add_task WHERE user_id = %s AND id = %s', (session['user_id'],id))
    task= cursor.fetchone()
    cursor.close()
    return render_template('diplay_data.html',task=task,id=id)

# update task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    title= request.form['title']
    due_date=request.form['due_date']

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE add_task SET title=%s, due_date=%s WHERE user_id= %s AND id=%s',(session['user_id'],title,due_date,id))
    mysql.connection.commit()

    cursor.close()
    
    return redirect(url_for('display_all'))
# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

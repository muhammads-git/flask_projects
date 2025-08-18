from flask import Flask, render_template, url_for, request, redirect, session
from flask import flash,get_flashed_messages
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt


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
app.secret_key = 'abc123cba321'

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form['Username'].strip()
        password = request.form['Password'].strip()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # handle empty username or password
        if username == '' or password == '':
            error = "Fields cannot be empty."

            return render_template('register.html', error=error)
        

        # else 
        # send data to database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

           
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None   # flag to send to template

    if request.method == 'POST':
        username = request.form['Username'].strip()
        password = request.form['Password'].strip()

        # if empty username or password
        if username == '' or password == '':
            error = "Fill in the fields."


            return render_template('login.html', error= error)
            
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            stored_hash = user[2]
            if bcrypt.check_password_hash(stored_hash, password):
                session['username'] = username
                return redirect(url_for('display_all'))
            else:
                error = "Password in incorrect"
        else:
            error = "Username not found, please register."
    return render_template('login.html')

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
    cursor.execute('SELECT * FROM add_task')
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
    cursor.execute('INSERT INTO add_task (title,due_date) VALUES (%s,%s)', (new_task,due_date))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))

@app.route('/remove_task', methods=['POST'])
def task_to_remove():
    if 'username' not in session:
        return redirect(url_for('login'))

    remove_title = request.form['remove_title']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM add_task WHERE title = %s', (remove_title,))
    
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))

@app.route('/mark_as_done', methods=['POST'])
def mark_as_done():
    if 'username' not in session:
        return redirect(url_for('login'))

    task_id = request.form['task_done']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE add_task SET is_done = 1 WHERE id = %s', (task_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('display_all'))


# edit task
@app.route('/edit/<int:id>', methods=["GET"])
def edit(id):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM add_task WHERE id = %s', (id,))
    task= cursor.fetchone()
    cursor.close()
    return render_template('diplay_data.html',task=task,id=id)

# update task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    title= request.form['title']
    due_date=request.form['due_date']

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE add_task SET title=%s, due_date=%s WHERE id=%s',(title,due_date,id))
    mysql.connection.commit()

    cursor.close()
    
    return redirect(url_for('display_all'))
# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

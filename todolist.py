from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

# create app object
app = Flask(__name__)
# configure flask to database
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'muhammad'
app.config['MYSQL_PASSWORD'] = '034971'
app.config['MYSQL_DB'] = 'todo'
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
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

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
        username = request.form['Username']
        password = request.form['Password']

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
    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))    # redirect to login


@app.route('/display_all', methods=['GET'])
def display_all():
    # if the user didnt login dont show this route
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM add_task')
    all_data = cursor.fetchall()
    cursor.close()

    return render_template('diplay_data.html', mydata=all_data)

@app.route('/task_to_add', methods=['POST'])
def task_to_add():
    if 'username' not in session:
        return redirect(url_for('login'))

    new_task = request.form['title']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO add_task (title) VALUES (%s)', (new_task,))
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

# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(debug=True)

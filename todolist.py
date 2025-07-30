from flask import Flask , render_template, url_for,request,redirect
from flask_mysqldb import MySQL

# create app object
app = Flask(__name__)
# configure flask to databses
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] ='muhammad'
app.config['MYSQL_PASSWORD'] = '034971'
app.config['MYSQL_DB'] = 'todo'
mysql = MySQL(app)

# first page
@app.route('/')
def page():
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM add_task'
    )
    titles = cursor.fetchall()
    cursor.close()

    return render_template('add_task.html',titles = titles)


#todo
@app.route('/enter_task',methods = ['POST','GET'])
def task_to_add():
    if request.method == 'POST':
        new_task= request.form['title']
    
    # sql 
    sql = 'INSERT INTO add_task (title) VALUES (%s)'
    val = (new_task,)

    #make connection
    cursor = mysql.connection.cursor()
    # insert
    cursor.execute(sql,val)

    # commit data
    mysql.connection.commit()

    # close cursor
    cursor.close()

    return redirect(url_for('display_all'))

# remove tasks 
@app.route('/remove_task', methods = ['POST','GET'])
def task_to_remove():
    if request.method == 'POST':
        remove_title = request.form['remove_title']

    # connection
    cursor = mysql.connection.cursor()
    # execute the values
    cursor.execute('DELETE FROM add_task WHERE title = %s', (remove_title,))
    # commit changes
    mysql.connection.commit()
    # close 
    cursor.close()
    
    return redirect(url_for('display_all'))

# task has been done
@app.route('/mark_as_done', methods=['POST'])
def mark_as_done():
    task_id = request.form['task_done']
    print("Task to mark as done: ",task_id)
    # make connection with mysql
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE add_task SET is_done = 1 WHERE id = %s', (task_id,))

    mysql.connection.commit()

    cursor.close()

    return redirect(url_for('display_all'))


@app.route('/display_all', methods=['GET'])
def display_all():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM add_task')
    all_data= cursor.fetchall()
    mysql.connection.commit()

    cursor.close()
    return render_template('diplay_data.html',mydata=all_data)

if __name__ == '__main__':
    app.run(debug=True)
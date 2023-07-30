from flask import Flask , render_template, request, redirect 
from flask_mysqldb import MySQL
import yaml


app=Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql=MySQL(app)

@app.route('/new_user', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        id = userDetails['id']
        name = userDetails['name']
        role = userDetails['role']
        email = userDetails['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, name, role, email) VALUES (%s, %s, %s, %s)", (id, name, role, email))
        mysql.connection.commit()
        cur.close()

        return redirect('/users')

    return render_template('index.html')



@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
    
@app.route('/users/<int:user_id>')
def get_user_details(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_details = cur.fetchone()
    cur.close()

    if user_details:

        return render_template('userdetails.html', user=user_details)
    else:
        return "User not found", 404


if __name__ == '__main__':
    app.run(debug=True)

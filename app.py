from audioop import add
from flask import Flask, render_template, request, redirect
from datetime import date
from flask_mysqldb import MySQL

app = Flask(__name__)
today = date.today()

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/')
def basic():
    return render_template('basic.html')

@app.route('/addpatients', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        Details = request.form
        pid = Details['pid']
        name = Details['name']
        mobile_number = Details['mobile_number']
        address = Details['address']
        city = Details['city']
        created_on = today
        updated_on = today
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients(pid, name, mobile_number, address, city, created_on, updated_on ) VALUES(%s, %s, %s, %s, %s, %s, %s)",(pid, name, mobile_number, address, city, created_on, updated_on))
        mysql.connection.commit()
        cur.close()
        return redirect('/displaypatients')
    return render_template('index.html')

@app.route('/displaypatients')
def patients():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM patients")
    if resultValue > 0:
        Details = cur.fetchall()
        return render_template('users.html',Details=Details)
    else:
        return 0;

@app.route('/addappointment', methods=['GET', 'POST'])
def aptms():
    if request.method == 'POST':
        # Fetch form data
        A_details = request.form
        aid = A_details['aid']
        pid = A_details['pid']
        appointment_date = A_details['appointment_date']
        purpose = A_details['purpose']
        status = A_details['status']
        created_on = today
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO appointments(aid, pid, appointment_date, purpose, status, created_on ) VALUES(%s, %s, %s, %s, %s, %s)",(aid, pid, appointment_date, purpose, status, created_on ))
        mysql.connection.commit()
        cur.close()
        return redirect('/displayappointment')
    return render_template('aptms.html')

@app.route('/displayappointment')
def fun():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM appointments")
    if resultValue > 0:
        A_details = cur.fetchall()
        return render_template('disp.html',A_details=A_details)
    else:
        return 0;

if __name__ == '__main__':
    app.run(debug=True)
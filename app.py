from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)

#Configure db
db = yaml.full_load(open(r'C:\Users\Vinutha TJ\OneDrive\Desktop\DBMS Project\Movie\loginform\db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        #The form data is stored in a variable called userDetails and request.form fetches the data from the HTML page
        userDetails = request.form
        username = userDetails['username']   
        name = userDetails['name']
        password = userDetails['password']
        birth = userDetails['birth']
        gender = userDetails['gender']
        subscription = userDetails['subscription']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USER(USERNAME,NAME,PASSWORD,PASSWORD_CONFIRM,DATEOFBIRTH,GENDER,SUBSCRIPTION) VALUES (%s,%s,%s,%s,%s,%s,%s)",(username,name,password,password,birth,gender,subscription))
        mysql.connection.commit()
        cur.close()
        return 'Sign up successful! Thank you for signing up'

    return render_template('house.html')


if __name__ == '__main__':
    app.run(debug=True)
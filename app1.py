from flask import Flask, render_template, request,session,redirect,url_for
from flask_mysqldb import MySQL
import yaml
import pymysql

app = Flask(__name__)
app.secret_key = "super secret key"
db = yaml.full_load(open(r"C:\Users\Vinutha TJ\OneDrive\Desktop\DBMS Project\Movie\Main page\db.yaml"))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        query_val = userDetails['query']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO QUERY(QUERY_VAL) VALUES(%s)",(query_val,))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')

@app.route('/second',methods=['GET', 'POST'])
def house():
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
        val = "Sign up successful! Thank you for signing up, your details include: Name: {0}, Password: {1}, Date-of-Birth: {2}, Gender: {3}, Subscription: {4}".format(name,password,birth,gender,subscription)
        return val
    return render_template('house.html')


#After login success
@app.route('/booking',methods=['GET', 'POST'])
def booking():
    #After
    msg=''
    #After
    if request.method == 'POST':
        #The form data is stored in a variable called userDetails and request.form fetches the data from the HTML page
        userDetails = request.form
        ticketid = userDetails['ticketid']   
        username = userDetails['username']
        movietitle = userDetails['movietitle']
        date = userDetails['date']
        time = userDetails['time']
        price = userDetails['price']
        payment = userDetails['payment']
        cur = mysql.connection.cursor()
        #After
        cur.execute('SELECT * FROM MOVIES WHERE MOV_TITLE=%s',[movietitle])
        record = cur.fetchone()
        if record:
            cur.execute("INSERT INTO TICKETS(TICKET_ID,USERNAME,MOVIE_TITLE,BOOK_DATE,BOOK_TIME,PRICE,PAYMENT_MODE) VALUES (%s,%s,%s,%s,%s,%s,%s)",(ticketid,username,movietitle,date,time,price,payment))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('logout'))
        else:
            msg = 'Incorrect moviename Try again!!'
            return msg
    return render_template('booking.html',msg=msg)
        #After
        #cur.execute("INSERT INTO TICKETS(TICKET_ID,USERNAME,MOVIE_ID,MOVIE_TITLE,BOOK_DATE,BOOK_TIME,PRICE,PAYMENT_MODE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(ticketid,username,movieid,movietitle,date,time,price,payment))
        #mysql.connection.commit()
        #cur.close()
        #return redirect(url_for('logout'))
    #return render_template('booking.html')


#Admin Update
@app.route('/adminupdate',methods=['GET', 'POST'])
def adminupdate():
    if request.method == 'POST':
        #The form data is stored in a variable called userDetails and request.form fetches the data from the HTML page
        userDetails = request.form
        mov_title = userDetails['mov_title']
        mov_year = userDetails['mov_year']
        mov_lang = userDetails['mov_lang']
        dir_id = userDetails['dir_id']
        duration = userDetails['duration']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MOVIES(MOV_TITLE,MOV_YEAR,MOV_LANG,DIR_ID,DURATION) VALUES (%s,%s,%s,%s,%s)",(mov_title,mov_year,mov_lang,dir_id,duration))
        mysql.connection.commit()
        cur.close()
        val = "Updation successful! Thank you for signing up, your details include: Movie Title: {0}, Movie Year: {1}, Movie Language: {2}, Director ID: {3}, Duration: {4}".format(mov_title,mov_year,mov_lang,dir_id,duration)
        return redirect(url_for('logout'))
    return render_template('adminupdate.html')       

#This goes for booking tickets slot when login is successful for user
@app.route("/index")
def main_page():
    return render_template('index.html',username = session['username'])


#This is for user's login
@app.route("/login",methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM USER WHERE USERNAME=%s AND PASSWORD=%s',(username,password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[0]
            return redirect(url_for('booking'))
        else:
            msg = 'Incorrect username/password. Try again!!'
    return render_template('login.html',msg=msg)

#This is for admin's login
@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM ADMIN WHERE USERNAME=%s AND PASSWORD=%s',(username,password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[0]
            #Redirect's to uploading movies in theatre
            return redirect(url_for('adminupdate'))
        else:
            msg = 'Incorrect username/password. Try again!!'
    return render_template('adminlogin.html',msg=msg)


#Logout for users
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

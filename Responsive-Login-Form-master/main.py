from flask import Flask, render_template, request, redirect, session, url_for, flash
import os
from flask_mysqldb import MySQL
import random as r

# use of Session Module
app = Flask(__name__)
app.secret_key = os.urandom(24)

# sql connnection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '**********'
# app.config['MYSQL_DB'] = 'price_tracker'

mysql = MySQL(app)

uid = 1


# redirect module is used below
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    print("yes")
    usern = request.form['username']

    # sql connection part
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from login")
    # password manager
    # use a random number generator and not in list and generate

    data = cur.fetchall()
    password = ""
    username = usern
    # uid=0
    global uid

    for tup in data:
        print(tup)

        if (tup[1] == usern):
            print("*****")
            password = tup[2]
            uid = tup[0]

            print(f'{uid} -------')

    if request.form['password'] == password and request.form['username'] == username:
        print("logged in")
        session['logged_in'] = True
        return redirect(url_for('home', usern=usern))
    else:
        return 'Invalid Credentials. Please try again.'


#    try to put a main page redirection link here or let it not pass the main page


@app.route('/<usern>')
def home(usern):
    # sort out passing of uid
    print(usern)
    print(uid)

    # use product table here

    cur = mysql.connection.cursor()
    # cur.execute("SELECT * from product")
    cur.execute('SELECT * FROM login WHERE username = %s', (usern,))
    usr = cur.fetchall()
    print(f"{usr} not")
    cur.execute('SELECT * FROM product WHERE user_id = %s', (uid,))
    data = cur.fetchall()
    # cur.execute("SELECT username from login where user_id=%s",uid)
    # data_user =cur.fetchone()

    print(data)

    # dummy values
    # consider a case where u find no product
    product = {'product_id': 1,
               'user_id': 1,
               'name': "none",
               'url': "google.com",
               'price': '0'
               }

    l = []
    #
    for tup in data:
        product = {'product_id': tup[0],
                   'user_id': tup[1],
                   'name': tup[2],
                   'url': tup[3],
                   'price': tup[4]
                   }
        l.append(product)

    if 'logged_in' in session:
        return render_template('user.html', usern=usern, all_products=l)
    else:
        return redirect('/')


@app.route('/signup')
def sign():
    print('came here')
    return render_template('sign_up.html')


@app.route('/info', methods=['POST'])
def info():
    #     store submitted info here

    print("got it")
    username = request.form['username']
    password = request.form['password']
    phone = request.form['number']
    email = request.form['email']
    userid = 0

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id from login")
    data = cur.fetchall()
    print(data)
    data = list(data)

    while (True):
        userid = r.randint(1, 100)
        if userid not in data:
            break

    cur.execute("insert into user values (%s,%s,%s)", (userid, email, phone))
    cur.execute("insert into login values (%s,%s,%s)",
                (userid, username, password))

    print(username)
    print(userid)
    print(password)
    print(phone)

    mysql.connection.commit()

    # implement stored procedure here
    # and trigger at necessary place to enter value
    print("inserted values")

    return redirect('/')


@app.route('/product_details')
def product_details():
    return render_template('product_det.html')


@app.route('/insert', methods=['POST'])
def insert():
    # if request.method == "POST":

    flash("Data Inserted Successfully")
    product_name = request.form['product_name']
    product_url = request.form['product_url']
    expected_price = request.form['product_price']
    cur_price = request.form['price']
    cur = mysql.connection.cursor()
    cur.execute('SELECT Product_id FROM product WHERE user_id = %s', (uid,))
    data = cur.fetchall()
    print(data)
    data = list(data)

    product_id = 0

    while True:
        product_id = r.randint(1, 100)
        if product_id not in data:
            break
    # stored Procedure
    cur.callproc('add_product', (product_name, product_url,
                                 expected_price, cur_price, uid, product_id))
    # cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


# run the program
if __name__ == '__main__':
    app.run(debug=True)

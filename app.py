# import flask and its library
from flask import Flask, redirect, request, url_for, render_template, flash, session
import sqlite3
import sys
# the Flask app
app = Flask(__name__)
# set secret_key needed to view session details
app.secret_key = "super secret key"
# file for the Database
DB_FILE = 'mydb.db'

# Error handling page template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# rendering homepage
@app.route('/')
def index():
    return render_template('index.html')

# render phonedatabase.html
@app.route('/phonedatabase')
def phoneDatabase():
    return render_template('phonedatabase.html')

# render aboutus.html
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# rendering s9+.html with comments on the page
@app.route('/phones/s9+', methods=['POST', 'GET'])
def s9():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM s9_comments")
        rv = cursor.fetchall()
        cursor.close()
        return render_template("s9+.html", entries=rv, usernamevalue=session['username'])
    except:
        return render_template("404.html", errormsg=sys.exc_info())


# insert comments into the s9_comments table
def s9_comments(username, user_comment):
    """
    put a new entry in the database
    """
    params = {'username': username,
              'user_comment': user_comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "insert into s9_comments VALUES (:username, :user_comment)", params)
    connection.commit()
    cursor.close()


# call the method to insert comments into the s9_comments table and redireact to the s9+.html page after comment is posted
@app.route('/post-comment-s9', methods=['POST'])
def post_comment_s9():
    s9_comments(request.form['username'],
                request.form['user_comment'])
    return redirect(url_for('s9'))

# rendering s10.html with comments on the page
@app.route('/phones/s10', methods=['POST', 'GET'])
def s10():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM s10_comments")
        rv = cursor.fetchall()
        cursor.close()
        return render_template("s10.html", entries=rv, usernamevalue=session['username'])
    except:
        return render_template("404.html", errormsg=sys.exc_info())

# insert comments into the s10_comments table


def s10_comments(username, user_comment):
    """
    put a new entry in the database
    """
    params = {'username': username,
              'user_comment': user_comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "insert into s10_comments VALUES (:username, :user_comment)", params)
    connection.commit()
    cursor.close()

# call the method to insert comments into the s10_comments table and redireact to the s9+.html page after comment is posted
@app.route('/post-comment-s10', methods=['POST'])
def post_comment_s10():
    s10_comments(request.form['username'],
                 request.form['user_comment'])
    return redirect(url_for('s10'))

# rendering iphone11.html with comments on the page
@app.route('/phones/iphone11', methods=['POST', 'GET'])
def iphone11():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM iphone11_comments")
        rv = cursor.fetchall()
        cursor.close()

        return render_template("iphone11.html", entries=rv, usernamevalue=session['username'])
    except:
        return render_template("404.html", errormsg=sys.exc_info())

# insert comments into the iphone11_comments table


def iphone11_comments(username, user_comment):
    """
    put a new entry in the database
    """
    params = {'username': username,
              'user_comment': user_comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "insert into iphone11_comments VALUES (:username, :user_comment)", params)
    connection.commit()
    cursor.close()

# call the method to insert comments into the iphone11_comments table and redireact to the s9+.html page after comment is posted
@app.route('/post-comment-iphone11', methods=['POST'])
def post_comment_iphone11():
    iphone11_comments(request.form['username'],
                      request.form['user_comment'])
    return redirect(url_for('iphone11'))

# render guestbook page
@app.route('/guestbook')
def guestbook():
    """
    An input form for signing the guestbook
    """
    return render_template("guestbook.html")

# insert guestbook comments


def insert_guestbook(name, email, comment):
    """
    put a new entry in the database
    """
    params = {'name': name, 'email': email, 'comment': comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "insert into guestbook VALUES (:name, :email, :comment)", params)
    connection.commit()
    cursor.close()

# function to run when guestbook comment is posted
@app.route('/sign', methods=['POST'])
def sign():
    """
    Accepts POST requests, and processes the form;
    Redirect to index when completed.
    """
    insert_guestbook(request.form['name'], request.form['email'],
                     request.form['comment'])
    return redirect(url_for('guestbook'))

# function to view comments on guestbook page
@app.route('/view', methods=['GET', 'POST'])
def view():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guestbook")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("guestbook-view.html", entries=rv)

# function to register user by inserting values in user table in sqlite3 with error messages if user is not successfully registered
@app.route('/user', methods=['POST'])
def insert_user():
    """
    put a new entry in the database
    """
    if request.method == "POST":
        username = request.form['username']
        name = request.form['name']
        user_email = request.form['user_email']
        age = request.form['age']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            params = {'username': username, 'name': name,
                      'user_email': user_email, 'age': age, 'password': password}
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute(
                "insert into users VALUES (:username, :name, :user_email, :age, :password)", params)
            connection.commit()
            cursor.close()
            return render_template('login-page.html', register_success="You've been successfully registered, please log in")
        else:
            return render_template("login-page.html", register_error="your passwords do not match, please retype")
    else:
        return redirect(url_for('login'))

# login method that assigns session with true after valudation user login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        query = "select * from users where username = '" + \
            request.form['username']
        query = query + "' and password = '" + request.form['password'] + "';"
        connection = sqlite3.connect(DB_FILE)
        cur = connection.execute(query)
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 1:
            session['username'] = request.form['username']
            session['logged in'] = True
            return render_template('index.html', login_success="Successfully Logged in")
        else:
            return render_template('login-page.html', login_error="Username/Password Incorrect!", usernamevalue=session['username'])
    else:
        return render_template('login-page.html')

# logout function that assigns session[logged in] with the value of false, and renders a message for user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged in'] = False
    return render_template('index.html', logout_msg="Successfully Logged out")


# if method that runs the python code with debug mode
if __name__ == "__main__":
    app.run(debug=True)

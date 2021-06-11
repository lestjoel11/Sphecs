# import flask and its library
from flask import Flask, redirect, request, url_for, render_template, flash, session
from bs4 import BeautifulSoup
import sqlite3
import sys
import requests
from datetime import date, datetime
# the Flask app
app = Flask(__name__)
# set secret_key needed to view session details
app.secret_key = "super secret key"
# file for the Database
DB_FILE = 'mydb.db'

# TRY AND EXCEPT CAN BE USED


class newsDB:
    def __init__(self, save_date, title, link=None):
        self.save_date = save_date
        self.title = title
        self.link = link

    def storeInformation(self):
        db = sqlite3.connect(DB_FILE)
        params = {'date': self.save_date,
                  'headline': self.title, 'link': self.link}
        db.execute(
            "insert or ignore into news_db values(:date, :headline, :link);", params)
        db.commit()


class weatherDB(newsDB):
    def storeInformation(self):
        db = sqlite3.connect(DB_FILE)
        params = {'saved_date_and_forecast_day': str(self.save_date),
                  'weather': self.title}
        db.execute(
            "insert or ignore into weather_db values(:saved_date_and_forecast_day, :weather);", params)
        db.commit()


class videoDB(newsDB):
    def storeInformation(self):
        db = sqlite3.connect(DB_FILE)
        params = {'saved_date': self.save_date, 'video_link': str(self.title)}
        db.execute(
            "insert or ignore into video_db values(:saved_date, :video_link);", params)
        db.commit()


# Error handling page template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# rendering homepage
@app.route('/')
def index():
    return render_template('index.html', )

# render phonedatabase.html
@app.route('/phonedatabase')
def phoneDatabase():
    return render_template('phonedatabase.html')


# render news.html
@app.route('/news')
def newsPage():
    # try except start
    try:
        # saving date to be stored in dB
        today = date.today()
        # using request to capture website
        webpage = requests.get("https://www.gsmarena.com/news.php3")
        # decoding webpage using html parser
        soup = BeautifulSoup(webpage.content, 'html.parser')
        # creating two dictionaries to store values of website scraping
        news = dict()
        allNews = dict()
        # counter variable
        counter = 1
        # for loop to read findAll method
        for x in soup.findAll('div', class_="news-item"):
            # storing scraped parts into dictionary
            news = {'pic': x.find("div", class_="news-item-media-wrap left").img["src"], 'title': x.find('h3').text, 'link': x.find(
                'a').text, 'caption': x.find('p').text, 'meta': x.find('div', class_="meta-line").span.text,
                'link': "https://www.gsmarena.com/" + x.find("div", class_="news-item-media-wrap left").a['href']}
            # storing news dictionary with key of value counter, so as to store all news from page
            allNews[counter] = news
            # incrementing counter to increase key value
            counter += 1
            # providing values for constructor of saveNews class
            saveNews = newsDB(today, news['title'], news['link'])
            # storing info in dB using function from newsDB class
            saveNews.storeInformation()
    # except return value of error 404
    except:
        return render_template("404.html", errormsg=sys.exc_info())
    # returning template news.html and news scraped
    return render_template('news.html', allNews=allNews, counter=counter)


@app.route('/top_brands')
def topBrands():
    try:
        samsung = requests.get(
            "https://www.britannica.com/topic/Samsung-Electronics")
        samsung_soup = BeautifulSoup(samsung.content, 'html.parser')
        britannia_info_samsung = samsung_soup.find('section', id="ref1")
        samsung_info = britannia_info_samsung.find_all('p')
        samsung_list = []
        for x in samsung_info:
            samsung_list.append(x)

        apple1 = requests.get(
            "https://www.britannica.com/topic/Apple-Inc")
        apple_soup1 = BeautifulSoup(apple1.content, 'html.parser')
        britannica_info_apple1 = apple_soup1.find('section', id="ref1")

        apple2 = requests.get(
            "https://www.britannica.com/topic/Apple-Inc/Apple-refocuses-on-key-markets")
        apple_soup2 = BeautifulSoup(apple2.content, 'html.parser')
        britannica_info_apple2 = apple_soup2.find('section', id="ref93003")
        apple_list = []
        for y in britannica_info_apple2.findAll('p'):
            apple_list.append(y)
    except:
        return render_template("404.html", errormsg=sys.exc_info())
    return render_template('top_brands.html', samsung_info=samsung_list, apple_info1=britannica_info_apple1, apple_info2=apple_list)

# route for the about us page
@app.route('/aboutus')
# render aboutus.html
def aboutus():
    # try except start
    try:
        # getting today's date from the library
        today = date.today()
        # request to scrape website
        webpage = requests.get(
            "https://forecast.weather.gov/MapClick.php?lat=37.31896000000006&lon=-122.02927999999997")
        # using html parser to read website
        soup = BeautifulSoup(webpage.content, 'html.parser')
        # scraping using css classes using select
        week = soup.select(".tombstone-container   .period-name")
        # saving text from week in a list
        days = [pt.get_text() for pt in week]
        # getting weather description in a list using select
        weather_desc = [sd.get_text() for sd in soup.select(
            ".tombstone-container .short-desc")]
        # getting a week's weather in a list using select
        week_weather = [t.get_text()
                        for t in soup.select(".tombstone-container  .temp")]

        count = 0
        # for loop to join date and daily temperature and store in database
        for x in days:
            # print(today, x, week_weather[count])
            dateAndForecastDay = str(today), x
            storeWeather = weatherDB(dateAndForecastDay, week_weather[count])
            storeWeather.storeInformation()
            count += 1
    # try except end with error page returning
    except:
        return render_template("404.html", errormsg=sys.exc_info())
    return render_template('aboutus.html', days=days, week_weather=week_weather, weather_desc=weather_desc)

# route for the video page
@app.route('/videos')
# videos page function
def videos():
    # try except start
    try:
        # date using date library to store in dB
        today = date.today()
        # webpage request
        webpage = requests.get("https://www.gsmarena.com/videos.php3")
        # html parsing the requested webpage
        soup = BeautifulSoup(webpage.content, 'html.parser')
        # find all iframe videos
        videos = soup.find_all('iframe')
        # for loop to get all iframe src links
        for x in videos:
            vid_link = 'https:'+x['src']
            # creating object with constructors
            storeLinks = videoDB(today, vid_link)
            # storing date and vid_link in db
            storeLinks.storeInformation()
    # try except end with error page
    except:
        # render error template
        return render_template("404.html", errormsg=sys.exc_info())
    return render_template('videos.html', videos=videos)

# rendering s9+.html with comments on the page
@app.route('/phones/s9+', methods=['POST', 'GET'])
def s9():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM s9_comments")
        rv = cursor.fetchall()
        cursor.close()
        webpage = requests.get(
            "https://www.mobilephonesspecs.com/samsung-galaxy-s9/")
        soup = BeautifulSoup(webpage.content, 'html.parser')
        table_info = soup.find_all('td')
        return render_template("s9+.html", entries=rv, usernamevalue=session['username'], table_info=table_info)
    except:
        return render_template("404.html", errormsg="sys.exc_info()", error_code="Please sign in to view")


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
    session['username'] = None
    return render_template('index.html', logout_msg="Successfully Logged out")


# if method that runs the python code with debug mode
if __name__ == "__main__":
    app.run(debug=True)

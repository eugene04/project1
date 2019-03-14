import os
import requests

from flask import Flask, session, render_template, request, flash , redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)



# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://styplpqwmqycvb:9f6a39d6d6ae1fcd842a65f2e94b2c46eafc5cab13176650271d6413d446ac99@ec2-23-21-128-35.compute-1.amazonaws.com:5432/d5m4q2tv0ld4f4")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html')
    


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        if db.execute("SELECT * FROM users WHERE email= :email AND password= :password",{'email':email,'password':password}).rowcount==0:
            flash('check your email address and password and try again','danger')
            
        else:
            flash(f'{email} you are now logged in','success')
            return redirect (url_for('books'))
    return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def register(): 
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        db.execute("INSERT INTO users (email,password) VALUES(:email, :password)",{"email":email,           "password":password})
        db.commit()
        flash(f'congratulations {email} you have successfully registered for our site and are now logged in','success')
        return redirect (url_for('books'))
    return render_template("register.html")
    
@app.route("/search",methods=['GET','POST'])
def search():
    books=db.execute("SELECT * FROM books ").fetchall() 
    return render_template('search.html', books=books)

@app.route("/details/<int:book_id>", methods=["GET", "POST"])
def details(book_id):
    books=db.execute("SELECT * FROM books WHERE id=:book_id",{'book_id':book_id}).fetchone()
    
    res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"k3SrIbt8oJkVU4V0E34dA","isbns":books.isbn}).json()["books"][0]
    work_ratings_count = res["work_ratings_count"]
    average_rating = res["average_rating"]
    isbn = res["isbn"]
    return render_template('details.html', books=books , work_ratings_count=work_ratings_count ,average_rating=average_rating , isbn=isbn)

     


@app.route("/books",methods=['GET','POST'])
def books():
    books=db.execute("SELECT * FROM books ").fetchall() 
    return render_template('mybooks.html',books=books)

@app.route("/mybooks",methods=['GET','POST'])
def mybooks():
    if request.method == "POST":
        searchtype=request.form.get('searchtype')
        query=request.form.get('query')
        if searchtype=='author':
            books = db.execute("SELECT * FROM books WHERE author = :query", {"query": query}).fetchall()
        elif searchtype=='isbn':
            books = db.execute("SELECT * FROM books WHERE isbn = :query", {"query": query}).fetchall()
        elif searchtype=='title':
            books = db.execute("SELECT * FROM books WHERE title = :query", {"query": query}).fetchall()
        else :
            books = db.execute("SELECT * FROM books WHERE year = :query", {"query": query}).fetchall()
    
    return render_template('mybooks.html', books=books )
    
    

             
        
if __name__=='__main__':
    app.run(debug=True)

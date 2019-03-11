import os

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
    books=db.execute("SELECT * FROM books").fetchall() 
    return render_template('index.html',books=books)
    


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
    if request.method == "POST":
        author=request.form.get('author')
        book=db.execute("SELECT * FROM books WHERE author=:author",{'author':author}).fetchall()
        return redirect (url_for('details'))
    return render_template("search.html")
    

    


@app.route("/books",methods=['GET','POST'])
def books():
    books=db.execute("SELECT * FROM books ").fetchall() 
    return render_template('books.html',books=books)

             
        
if __name__=='__main__':
    app.run(debug=True)

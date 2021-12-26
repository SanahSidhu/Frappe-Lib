from flask import Flask, g, redirect, render_template, request, session
from dotenv import load_dotenv
import sqlite3 as s
import requests
import os

from .utils import issue_book, return_book
from mainapp.models import (
    chk_admin_exist,
    create_member,
    create_issue, 
    check_errors,
    get_email,
    chk_pass
)



load_dotenv()

pool_request = requests.Session()
url = 'https://frappe.io/api/method/frappe-library'


path = "sample.db"


create_member(path)
create_issue(path)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.before_request
def security():
    g.user = None
    if 'user_email' in session:
        emails = get_email(path)
        try:
            useremail = [
                email for email in emails if email[0] == session["user_email"]
            ][0]
            g.user = useremail
        except Exception as e:
            print(e)



@app.route("/", methods = ["GET","POST"])
def home():
    """
    Login Page
    """

    session.pop("user_email", None)

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        if chk_admin_exist(path,email):
            print("exists")
            if chk_pass(path,email, password):
                session['user_email'] = email
                print("correct")
                return redirect("/index")
            else:
                return render_template(
                        "login.html", error="Incorrect Email or Password")

        return render_template("login.html", error="You are not an Admin")
    else:
        return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    """
    Home Page
    """
    if g.user:
        return render_template("home.html")
    return redirect("/")


@app.route("/issue", methods = ["GET", "POST"])
def issuepg():
    if g.user:
        if request.method == "POST":
            try:
                debt = int(request.form.get('debt'))
                email = request.form.get('email')
                isbn = request.form.get('isbn')

            except Exception as e:
                print(e)
                return render_template("issue.html", error = e)
            
            params = {
                "isbn": isbn
            }

            response = pool_request.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if result := check_errors(data=data):
                    print(result)
                    if not isinstance(result, dict):
                        return render_template("issue.html", not_available=True)
                else:
                    if issue_book(path,isbn,email, debt):
                        return render_template("issue.html", available = True)
                    else:
                        return render_template("issue.html", issue_error = True )
            else:
                return render_template("issue.html", not_available = True)
        else:
            return render_template("issue.html")
    return redirect("/")


@app.route("/return", methods = ["GET", "POST"])
def returnpg():
    if g.user:
        if request.method == "POST":
            try:
                isbn = request.form.get('isbn')
                email = request.form.get('email')
                fee = request.form.get('fee')
            except Exception as e:
                print(e)
                return render_template("return.html", error = e)
            
            if return_book(path, isbn, email, fee):
                return render_template("return.html", return_true = True)
            else:
                return render_template("return.html", return_false = True)
        else:
            return render_template("return.html")
    return redirect("/")


@app.route("/search", methods = ["GET", "POST"])
def searchpg():
    if g.user:

        if request.method == "POST":
            try:
                author = request.form.get('author')
                title = request.form.get('title')
               
            except Exception as e:
                return render_template("search.html", error = e)
            
            params = {
                "author": author,
                "title": title
            }

            response = pool_request.get(url, params=params)
            if response.status_code == 200:
                print("200 received")
                data = response.json()

                if result := check_errors(data):
                    print(result)
                    if not isinstance(result, dict):
                        return render_template("search.html", not_found = True)
                else:
                    book_isbn = data['message'][0]['isbn']
                    fres = f"Book Found! Issue using ISBN code: {book_isbn}"
                    print("fres")
                    return render_template("search.html", found = True, msg = fres )
        else:
            return render_template("search.html")
    return redirect("/")

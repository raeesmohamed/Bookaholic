import requests
from flask import render_template, redirect,request, Blueprint

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/index", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = requests.get("https://www.googleapis.com/books/v1/volumes?q=inauthor:" + request.form.get('books')+"&key=AIzaSyCFkltepTLq1bnaYuZmK9x9_J4DtZciNzg").json()
        redirect('index.html')
        return render_template('search.html', books = req)
    return render_template("index.html", title = 'home')

"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

#from crypt import methods
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mySecretKey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
     #class variable
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(25), unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_passowrd(self, password):
        return check_password_hash(self, password)
        

    


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def index():
    """Renders a sample page."""
    #return "Hello World!"
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

#Login
@app.route('/login', methods = ["POST"])
def login():
    # kolek info dari form
    username = request.form['username']
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        pass
    else:
        return render_template("index.html")
    


#Register


#Dashboard


#Logout



if __name__ == '__main__':
    import os
    with app.app_context():
        db.create_all()            
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)

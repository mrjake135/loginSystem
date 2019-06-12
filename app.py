from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = ''
app.config['USE_SESSION_FOR_NEXT'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You really need to log in"
login_manager.username_message = "Username already Used"
login_manager.password_message = "Password already Used"


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logmein', methods = ['POST'])
def logmein():
    username = request.form['username']
    passwordform = request.form['password']
    user = User.query.filter_by(username=username).first()

    if not user:
        return '<h1> User not found! </h1>'

    if (user.password != passwordform):
        return '<h1> Incorrect Password </h1>'

    login_user(user)

    return '<h1> You are now logged in! </h1>'

# @app.route('/')
# def index():
#     user = User.query.filter_by(username = 'Anthony').first()
#     login_user(user)
#     return 'You are now logged in'
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out'

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerme', methods = ['POST'])
def registerme():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        return '<h1>User already exists you fucking ape</h1>'
    else:
        newUsername = request.form['username']
        newPassword = request.form['password']
        newUser = User(username=newUsername,password = newPassword)
        db.session.add(newUser)
        db.session.commit()
        return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return 'The current user is ' + current_user.username

if __name__ == "__main__":
    app.run(debug = True)

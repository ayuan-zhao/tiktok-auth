from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import LoginForm
from users import User
from datetime import timedelta
import os
app = Flask(__name__)
app.debug = True
# Set the session expiration time to 24 hours
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.secret_key = os.urandom(24)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * from login_user where user_id = (?)", [user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2])


@app.route("/", methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Home Page')


@app.route("/profile", methods=['GET'])
@login_required
def profile():
    print(current_user.email)
    print("---------- get profile ---------------")
    flash('Welcome ' + current_user.email)
    print("---------- get end ---------------")
    return render_template('profile.html', title='Login Successful')


@app.route("/login", methods=['GET'])
def login():
    print("---------- get dologin ---------------")
    if current_user.is_authenticated:
        print("-- The user already logged in.--")
        return redirect(url_for('profile'))
    print("---------- get dologin end---------------")
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    print("---------------------- logout user ----------------------")
    logout_user()
    print("---------------------- logout user end ----------------------")
    return redirect(url_for('login'))


@app.route("/dologin", methods=['POST'])
def dologin():
    print("---------- post dologin ---------------")
    form = request.form
    print('Validate on submit')
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM login_user where email = (?)",
                [form.get('email')])
    user = list(curs.fetchone())
    Us = load_user(user[0])
    if form.get('email') == Us.email and form.get('password') == Us.password:
        login_user(Us, remember=True)
    #   Umail = list({form.email.data})[0].split('@')[0]
    #   flash('Logged in successfully '+Umail)
        print("---------- post dologin succ----------------------")
        return redirect(url_for('profile'))    
    else:
        flash('Login Unsuccessfull.')

    print("---------- post dologin failed----------------------")
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)

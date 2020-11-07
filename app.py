from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm

app = Flask(__name__)
# calling Flask class 

# connect to specific database in postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key9876"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def handle_register_form():
    form = RegisterUserForm()

    # If POST & form valid
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        
        session['username'] = new_user.username

        return redirect('/')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def handle_login():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if (User.authenticate(username, password)):
            session['username'] = username
            return redirect(f"/users/{username}")
    
    return render_template('login.html', form=form)



@app.route('/users/<username>')
def show_secret_page(username):
    """show logged in user, their user info"""
    if 'username' in session:
        user = User.query.filter_by(username=username).first()
        return render_template('user_info.html', user=user)
    else:
        return render_template('no_auth.html')

@app.route('/logout')
def logout_user():
    """clear session and redirect"""
    if 'username' in session:
        session.pop('username')

    return redirect('/')

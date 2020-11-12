from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized

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

        return redirect(f"/users/{username}")

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

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user from database, delete all feedback, remove from session """
    if 'username' not in session or username != session['username']:
        raise Unauthorized()    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()        
    session.pop('username')

    flash(f'{username} deleted', 'success')
    return redirect('/')
  


@app.route('/users/<username>')
def show_secret_page(username):
    """show logged in user, their user info"""
    if 'username' in session:
        user = User.query.filter_by(username=username).first()
        feedback = user.feedback
        return render_template('user_info.html', user=user, feedback=feedback)
    else:
        raise Unauthorized()
    
@app.route('/logout')
def logout_user():
    """clear session and redirect"""
    if 'username' in session:
        session.pop('username')

    flash('You have successfully logged out', 'success')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def handle_add_feedbackform(username):
    form = FeedbackForm()

    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/register')

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def handle_update_feedback(feedback_id):
    """Show update-feedback form and process it."""
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']: 
        raise Unauthorized()

    form = FeedbackForm(obj=feedback_id)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template('edit_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def handle_delete_feedback(feedback_id):
    """Delete feedback."""
    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']: 
        raise Unauthorized()

    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback) 
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template('edit_feedback.html', form=form, feedback=feedback)

@app.errorhandler(401)
def show_unauthorized(e):
    """show 401 Unauthorized """
    return render_template('401.html'), 401

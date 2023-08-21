from flask_app import app
from flask import render_template,request,redirect,session
from flask import flash
from flask_app.models import event
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template("register_login.html")

# a route to register a user
@app.route('/register',methods=['POST'])
def register():
    if not user.User.validate_login(request.form):
        return redirect('/')
    password=request.form['password']
    if not password:
        return redirect('/')
    pw_hash=bcrypt.generate_password_hash(password)
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user_info=user.User.save(data)
    session['user_id']=user_info
    return redirect('/')

# a route for a user to log in using correct info
@app.route('/login',methods=['POST'])
def login():
    data={'email':request.form['email']}
    user_email=user.User.use_email(data)
    if not user_email:
        flash("Invalid email/ password",'error2')
        return redirect('/')
    user_password=user_email.password
    if not bcrypt.check_password_hash(user_password,request.form['password']):
        flash("Invalid password",'error2')
        return redirect('/')
    session['user_id']=user_email.id
    return redirect('/all_events')

# a route to get all shows presented
@app.route('/all_events')
def all_events():
    if 'user_id' not in session:
        return redirect('/logoff')
    data={
        'id':session['user_id']
    }
    user_id=user.User.get_userinfo_by_id(data)
    all_events=event.Event.get_all_events()
    return render_template('all_events.html',
    user=user_id, all_events=all_events)

@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('/')



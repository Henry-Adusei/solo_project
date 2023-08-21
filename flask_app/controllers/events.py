from flask_app import app
from flask import render_template,request,redirect,session
from flask import flash
from flask_app.models import event
from flask_app.models import user
from flask_app.controllers import users
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/new_event')
def new_event():
    if 'user_id' not in session:
        return redirect('/logoff')
    user_id= user.User.get_userinfo_by_id({'id':session['user_id']})
    return render_template('all_events.html',user=user_id)

@app.route('/add_event', methods=['POST'])
def add_event():
    if not event.Event.validations(request.form):
        return redirect('/all_events')
    user_id=user.User.get_userinfo_by_id({'id':session['user_id']})
    data={
        'event_title': request.form['event_title'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date_time': request.form['date_time'],
        'user_id':user_id.id
    }
    event.Event.save(data)
    return redirect('/all_events')

@app.route('/events/edit/<int:event_id>')
def edit_event(event_id):
    if 'user_id' not in session:
        return redirect('/logoff')
    data={
        'event_id':event_id
    }
    one_event=event.Event.get_event_by_id(data)
    user_id={'id':session['user_id']}
    return render_template('edit_event.html',one_event=one_event,user=user.User.get_userinfo_by_id(user_id))

@app.route('/update/<int:event_id>',methods=['POST'])
def update(event_id):
    if not event.Event.validations(request.form):
        return redirect(f"/events/edit/{event_id}")
    data={
        'event_title': request.form['event_title'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date_time': request.form['date_time'],
        'event_id': event_id
    }
    event.Event.update(data)
    return redirect('/all_events')

@app.route('/events/<int:event_id>')
def show_event(event_id):
    if 'user_id' not in session:
        return redirect('/logoff')
    user_id=user.User.get_userinfo_by_id({'id':session['user_id']})
    data={
        'event_id':event_id
    }
    one_event=event.Event.get_event_by_id(data)
    user_with_event=event.Event.get_event_with_user()
    return render_template('view_event.html',one_event=one_event,user=user_id,user_with_event=user_with_event)

@app.route('/delete/<int:event_id>')
def delete(event_id):
    if 'user_id' not in session:
        return redirect('/logoff')
    data={
        'event_id':event_id
    }
    event.Event.delete(data)
    return redirect('/all_events')

from flask_app.config.sqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime

class Event:
    def __init__(self,data):
        self.event_id=data['event_id']
        self.event_title=data['event_title']
        self.description=data['description']
        self.location=data['location']
        self.date_time=data['date_time']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.user=None

    def __repr__(self) -> str:
        return f"^^^^^ REPR- Method- event!! ====> {self.event_id,self.event_title,self.description,self.location,self.date_time,self.user}"

    @classmethod
    def save(cls,data):
        query="""
        INSERT
        INTO event(
            event_title,
            description,
            location,
            date_time,
            created_at,
            updated_at,
            user_id)
        VALUES(
            %(event_title)s,
            %(description)s,
            %(location)s,
            %(date_time)s,
            NOW(),
            NOW(),
            %(user_id)s);"""
        return connectToMySQL('events').query_db(query,data)

    # query to get all events
    @classmethod
    def get_all_events(cls):
        query="""
        SELECT *
        FROM event;
        """
        result=connectToMySQL('events').query_db(query)
        events=[]
        for event in result:
            events.append(cls(event))
        return events
    
    @classmethod
    def get_event_with_user(cls):
        query="""
        SELECT *
        FROM event
        JOIN user
        on event.user_id=user.id;
        """
        results=connectToMySQL('events').query_db(query)
        event_given=[]
        # using the same method as get_user_with_event
        for user1 in results:
            one_event=cls(user1)
            user_data={
                'id':user1['id'],
                'first_name':user1['first_name'],
                'last_name':user1['last_name'],
                'email':user1['email'],
                'password':user1['password'],
                'created_at':user1['created_at'],
                'updated_at':user1['updated_at']
            }
        one_event.user=user.User(user_data)
        event_given.append(one_event)
        return event_given

    @classmethod
    def get_event_by_id(cls,data):
        query="""
        SELECT *
        FROM event
        WHERE event_id=%(event_id)s;
        """
        return connectToMySQL('events').query_db(query,data)

    # an update query to make updated to events submitted
    @classmethod
    def update(cls,data):
        query="""
        UPDATE event 
        SET
        event_title=%(event_title)s,
        description=%(description)s,
        location=%(location)s,
        date_time=%(date_time)s,
        updated_at=NOW()
        WHERE
        event_id=%(event_id)s;
        """
        return connectToMySQL('events').query_db(query,data)

    # a delete method so a user can delete their submission if needed
    @classmethod
    def delete(cls,data):
        query="""
        DELETE
        FROM event
        WHERE event_id=%(event_id)s;
        """
        return connectToMySQL('events').query_db(query,data) 
    
    @staticmethod
    def validations(event):
        is_valid=True
        if len(event['event_title'])<3:
            flash("Event title must be at least 3 characters!!")
            is_valid=False
        if len(event['description'])<3:
            flash("Event description must be more than 3 characters!!")
            is_valid=False
        if len(event['location'])<3:
            flash("Location needs to be an actual place and more than 3 characters")
            is_valid=False
        if event['date_time']=='':
            flash("Please give event date and time")
            is_valid=False
        return is_valid

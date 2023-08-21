from flask_app.config.sqlconnection import connectToMySQL
from flask_app.models import event
from flask import flash
import re
import bcrypt

email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#creation of the user class
class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.event=None

    # prints the user id and first name in the terminal for checking
    def __repr(self) -> str:
        return f"###### REPR- Method- USERS ====> {self.id,self.first_name}"

    # saving the user into the database
    @classmethod
    def save(cls,data):
        query="""
        INSERT 
        INTO user(
            first_name,
            last_name,
            email,
            password,
            created_at,
            updated_at)
        VALUES(
            %(first_name)s,
            %(last_name)s,
            %(email)s,
            %(password)s,
            NOW(),
            NOW());"""
        return connectToMySQL('events').query_db(query,data)

    # to get the info of a specific user
    @classmethod
    def get_userinfo_by_id(cls,data):
        query="""
        SELECT * 
        FROM user 
        WHERE id=%(id)s;
        """
        result=connectToMySQL('events').query_db(query,data)
        if result and len(result)>0:
            return cls(result[0])
        else:
            return None

    # this is created to check and make sure a user does
    # not use the same email twice in validate_login
    @classmethod
    def use_email(cls,data):
        query="""
        SELECT *
        FROM user
        WHERE email=%(email)s;
        """
        result=connectToMySQL('events').query_db(query,data)
        if not result:
            return None
        return cls(result[0])

    # using of bcrypt to hash the password into the database
    @classmethod
    def get_hashed_pw(cls,data):
        query = "SELECT password FROM user where email = %(email)s;"
        result=connectToMySQL('events').query_db(query,data)
        if result:
            user_data=result[0]
            hashed_password= user_data['hashed_password']
            return hashed_password
        else:
            return None

    #doing validations for the different errors that may happen
    @staticmethod
    def validate_login(user):
        is_valid=True
        if len(user['first_name'])<3:
            flash("First name must be at least 3 characters!!!",'error1')
            is_valid=False
        if len(user['last_name'])<3:
            flash("Last name must be at least 3 characters!!!",'error1')
            is_valid=False
        # we use the get_email function here for checking to make sure the same email
        # is not used twice
        existing_user=User.use_email(user)
        if existing_user:
            flash("Please use a different email, Email already registered",'error1')
            is_valid=False
        if not email_regex.match(user['email']):
            flash("Invalid email address!",'error1')
        if len(user['password'])<8:
            flash("password must be at least 8 characters!!!",'error1')
            is_valid=False
        if user['password']!=user['confirm_password']:
            flash("Password and confirm password must match!!!",'error1')
            is_valid=False
        return is_valid

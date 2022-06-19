from flask_app import app
import re
from flask import session,flash
from flask_app.config.mysqlconnection import connectToMySQL,MySQLConnection
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = 'private_wall_schema'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        if User.validate_user(data):
            data = cls.parse_reg_data(data)
            query = """
                    INSERT INTO users (first_name,last_name,email,password)
                    VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
                    ;"""
            user_id = MySQLConnection(cls.db).query_db(query,data)
            session['user_id'] = user_id
            return user_id
        return False


    @classmethod
    def get_all_users(cls):
        query = """
                SELECT * FROM users
                ;"""
        results = MySQLConnection(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one_user(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                ;"""
        results = MySQLConnection(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
        


    @classmethod
    def get_user_by_email(cls,email):
        data = {'email': email}
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                ;"""
        results = MySQLConnection(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validate_user(user_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(user_data['first_name']) < 2:
            flash('* First name must be 3 characters.')
            is_valid = False
        if len(user_data['last_name']) < 3:
            flash('* Last name must be 3 characters.')
            is_valid = False
        if User.get_user_by_email(user_data['email'].lower()):
            flash('* Email is already taken.')
            is_valid = False
        if len(user_data['password']) < 8:
            flash('* Password must be atleast 8 characters.')
            is_valid = False
        if user_data['password'] != user_data['confirm_password']:
            flash('* Password do not match!')
            is_valid = False
        return is_valid
        
    @staticmethod
    def parse_reg_data(data):
        parsed_data = {
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'email':data['email'].lower(),
            'password':bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data

    @staticmethod
    def login(data):
        user = User.get_user_by_email(data['email'].lower())
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                return True
        flash('* Invalid Login info.')
        return False

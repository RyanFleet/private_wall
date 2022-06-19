from flask_app import app
from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL,MySQLConnection

class Message:
    db = 'private_wall_schema'
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.creator = data['creator']
        self.creator_id = data['creator_id']
        self.reciever = data['reciever']
        self.reciever_id = data['reciever_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_messages_with_creator(cls,data):
        query = """
                SELECT users.first_name 
                as creator, 
                users2.first_name 
                as reciever, messages.* FROM users
                LEFT JOIN messages 
                ON users.id = messages.creator_id
                LEFT JOIN users as users2
                ON users2.id = messages.reciever_id
                WHERE users2.id = %(id)s
                ;"""
        results = MySQLConnection(cls.db).query_db(query,data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages


    @classmethod
    def create_message(cls,data):
        query = """
                INSERT INTO messages (message,creator_id,reciever_id,user_id)
                VALUES (%(message)s,%(creator_id)s,%(reciever_id)s,%(user_id)s)
                ;"""
        return MySQLConnection(cls.db).query_db(query,data)

    @classmethod
    def delete_message(cls,data):
        query = """
                DELETE FROM messages 
                WHERE messages.id = %(id)s
                ;"""
        return MySQLConnection(cls.db).query_db(query,data)
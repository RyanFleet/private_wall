from crypt import methods
from flask_app import app
from flask import redirect,render_template,request,session
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route('/message/create', methods=['POST'])
def create_message():
    if 'user_id' in session:
        data={
            'user_id': session['user_id'],
            'creator_id': request.form['creator_id'],
            'message': request.form['message'],
            'reciever_id': request.form['reciever_id']
        }
        Message.create_message(data)
        return redirect('/user/wall')
    return redirect('/')


@app.route('/message/delete/<int:id>')
def delete_message(id):
    data = {'id':id}
    Message.delete_message(data)
    return redirect('/user/wall')
from crypt import methods
from flask import render_template,request,redirect,session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    if User.create_user(request.form):
        return redirect('/user/wall')
    return redirect('/')

@app.route('/user/wall')
def show_user_wall():
    if 'user_id' in session:
        data={'id':session['user_id']}
        user = User.get_one_user(data)
        messages = Message.get_all_messages_with_creator(data)
        users = User.get_all_users()
        return render_template('wall.html', messages=messages,users=users,user=user)
    return redirect('/user/logout')

@app.route('/user/login',methods=['POST'])
def login():
    if User.login(request.form):
        return redirect('/user/wall')
    return redirect('/')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')

from app import app
from model.user_model import UserModel
from flask import request, redirect, render_template, jsonify

obj = UserModel()

@app.route('/getallusers')
def getall_controller():
    return obj.getAllUsers()

@app.route('/register', methods=['GET', 'POST'])
def add_controller():
    if request.method == 'POST':
        data = request.form
        message = obj.addUser(data)
        if message == "User Added Successfully":
            return redirect('/login')
        return render_template('register.html', message=message)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = obj.login_user(email, password)

        if result['status'] == 'success':
            return redirect(f"/dashboard?name={result['name']}")
        else:
            return render_template('login.html', message="Invalid email or password")

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    name = request.args.get('name')
    if name:
        return render_template('dashboard.html', name=name)
    else:
        return redirect('/login')






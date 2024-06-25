from app import app 
from model.user_model import UserModel
from flask import request, redirect, render_template, jsonify

obj = UserModel()

@app.route('/getallusers')
def getall_controller():
    return obj.getAllUsers()

@app.route('/register', methods=['POST'])
def add_controller():
    data = request.form
    # return obj.addUser(data)
    message = obj.addUser(data)
    if message == "User Added Successfully":
        return redirect('/login')
    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # user_model = UserModel()
        result = obj.login_user(email, password)
        # user_model.close_connection()

        if result['status'] == 'success':
            return redirect(f"/dashboard?name={result['name']}")
        else:
            return render_template('login.html', message="Invalid email or password") 
        
    return render_template('login.html')





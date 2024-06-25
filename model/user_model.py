import psycopg2
import json
import bcrypt

class UserModel:
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host="localhost",
                user="username",
                password="password",
                database="db_name")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except Exception as e:
            print("Error in connection:", e)    

    def getAllUsers(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            return json.dumps(result)
        else:
            return "No Data Found"


    def addUser(self, data):
        try:
            # Check if the email already exists
            self.cur.execute("SELECT email FROM users WHERE email = %s", (data['email'],))
            result = self.cur.fetchone()
            
            if result:
                return "Email already exists 🤣, Try with a new email.."
            
            # Check if the password matches the confirmation password
            if data['password'] != data['ConfirmPassword']:
                return "Password doesn't match 😢..."
            
            # Hash the password
            hash_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Insert the new user into the database
            self.cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (data['name'], data['email'], hash_password)
            )
            self.con.commit()
            return "User Added Successfully"
        
        except Exception as e:
            print("Error:", e)
            return "An error occurred" 
        

    def login_user(self, email, password):
        try:
            # Check if the email exists
            self.cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = self.cur.fetchone()
            if user:
               # Check if the password matches
                password_match = bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8'))
                if password_match:
                    return {"status": "success", "name": user[1]}  
                else:
                    return {"status": "error", "message": "Invalid email or password"}
            else:
                return {"status": "error", "message": "User not found"}
        except Exception as e:
            print("Error:", e)
            return {"status": "error", "message": "Internal server error"}

         
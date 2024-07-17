import psycopg2
import json

class UserModel:
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="mysecretpassword",
                database="postgres",
                port=5432
            )
            self.con.autocommit = True
            self.cur = self.con.cursor()
            print("Connection Successful")
            # Create the table if it does not exist
            self.create_table()
        except Exception as e:
            print("Error in connection:", e)

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            s_no SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        '''
        try:
            self.cur.execute(create_table_query)
            print("Table 'users' created successfully.")
        except Exception as e:
            print("Error creating table:", e)

    def getAllUsers(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result) > 0:
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
            
            # Hash the password (consider using a hashing library like bcrypt)
            # hash_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Insert the new user into the database
            self.cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (data['name'], data['email'], data['password'])
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
                # Directly compare passwords (not recommended in production)
                if password == user[3]:  # Assuming user[3] is the password from the database
                    return {"status": "success", "name": user[1]}
                else:
                    return {"status": "error", "message": "Invalid email or password"}
            else:
                return {"status": "error", "message": "User not found"}
        except Exception as e:
            print("Error:", e)
            return {"status": "error", "message": "Internal server error"}

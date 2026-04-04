from flask import  Flask, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from db import init_db, get_connection


app = Flask(__name__)
app.secret_key ='secret123'
  
init_db()

@app.route("/")
def home():
    return " welcome to we app"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")


        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user =cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2],password):
            session["user"] =username
            return redirect("/dashboard")
            return "logged in successfully"
        else:
            return "Invalid credentials"
        
    return """
        <h2>Login</h2>
        <form method="post">
            <input name="username"><br><br>
            <input name="password" type="password"><br><br>
            <button>Login</button>
        </form>
    """

    


@app.route("/signup", methods=["GET", "POST"])

def  signup():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return "registered successfully "
        except:
            return "Username already exists"
        
        finally:
            conn.close()

    
    return """
        <h2>Signup</h2>
        <form method="post">
            <input name="username" placeholder="Enter username"><br><br>
            <input name="password" type="password" placeholder="Enter password"><br><br>
            <button type="submit">Signup</button>
        </form>
    """    

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    
    username = session.get('user')
    
    return f"""
        <h2>Dashboard{username}</h2>
        <p> You are logged in </p>
        <a href = '/logout'>Logout</a>
    """

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
    return redirect("login")





    













if __name__ == '__main__':
    app.run(debug =True)



from flask import  Flask, request, redirect

from db import init_db, get_connection


app = Flask(__name__)
  
init_db()

@app.route("/")
def home():
    return " Running successfully"



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
    
    return """
        <h2>Signup</h2>
        <form method="post">
            <input name="username" placeholder="Enter username"><br><br>
            <input name="password" type="password" placeholder="Enter password"><br><br>
            <button type="submit">Signup</button>
        </form>
    """    

if __name__ == '__main__':
    app.run(debug =True)



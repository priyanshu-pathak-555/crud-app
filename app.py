from flask import  Flask, flash, request, redirect, session, render_template
from streamlit import user
from werkzeug.security import generate_password_hash, check_password_hash


from db import init_db, get_connection


app = Flask(__name__)
app.secret_key ='secret123'
  
init_db()



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")


        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user =cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session["user"] = username
            session["user_id"] = user[0]
            flash("Logged in successfully")
            return redirect("/dashboard")
        else:
            flash("Invalid credentials")
            return redirect("/login")
        
    return render_template("login.html")

    


@app.route("/detect_account", methods=["GET", "POST"])
def detect_account():
    message = None
    account_exists = False
    if request.method == "POST":
        username = request.form.get("username")
        action = request.form.get("action")

        conn = get_connection()
        cursor = conn.cursor() 

        if action == "delete":
            
            cursor.execute("DELETE FROM notes WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
            
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            message = f"Account for '{username}' has been deleted."
        else:
           
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                account_exists = True
                message = f"Account found for username '{username}'."
            else:
                message = f"No account exists for '{username}'."

        conn.close()

    return render_template("detect_account.html", message=message, account_exists=account_exists, username=request.form.get("username") if request.method == "POST" else "")


@app.route("/signup", methods=["GET", "POST"])

def signup():
    if request.method =="POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            flash("Signup successful")
            return redirect("/login")
        except:
            flash("Username already exists")
            return redirect("/signup")
        finally:
            conn.close()

    
    return render_template("signup.html")
  

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notes WHERE user_id=?",
        (session["user_id"],)
    )

    notes = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session["user"],
        notes=notes
    )




@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
        session.pop("user_id", None)
        flash("Logged out successfully")
    return redirect("/login")








if __name__ == '__main__':
    app.run(debug =True)



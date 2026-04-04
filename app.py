from flask import  Flask, flash, request, redirect, session, render_template
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
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user =cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2],password):
            session["user"] =username
            flash("Logged in successfully")
            return redirect("/dashboard")
             
        else:
            flash("Invalid credentials")
            return redirect("/login")
        
    return render_template("login.html")

    


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
        flash("Logged out successfully")
    return redirect("login")




@app.route("/add_note", methods=["POST"])
def add_note():
    if "user_id" not in session:
        return redirect("/login")

    content = request.form.get("content")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (user_id, content) VALUES (?, ?)",
        (session["user_id"], content)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")



@app.route("/delete_note/<int:id>")
def delete_note(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/edit_note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        content = request.form.get("content")

        cursor.execute(
            "UPDATE notes SET content=? WHERE id=? AND user_id=?",
            (content, id, session["user_id"])
        )

        conn.commit()
        conn.close()
        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM notes WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )
    note = cursor.fetchone()
    conn.close()

    return render_template("edit_note.html", note=note)









if __name__ == '__main__':
    app.run(debug =True)



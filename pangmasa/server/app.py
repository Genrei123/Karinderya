from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "genrey"

# Database refer to SQLAlchemy
# This video: https://www.youtube.com/watch?v=uZnp21fu8TQ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Table model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index")
def home():
    # Check if the user has really logged in
    if "user" in session:

        user = session["user"]

        return render_template("index.html", user=user)

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_password")

        found_user = Users.query.filter_by(username = username).first()

        if password != confirm_pass:
            flash("Inputted passwords does not match", 'error')
            return render_template("register.html")
        elif found_user:
            flash("Username already exists", 'error')
            return render_template("register.html")

        # Saving data in the table
        # Refer to this video: https://www.youtube.com/watch?v=1nxzOrLWiic
        user = Users(username, password)
        db.session.add(user)
        db.session.commit()



    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print("test")

    else:
        if "user" in session:
            return redirect("/index")
        return render_template("login.html")


def logout():
    session.pop("user", None)
    return render_template("index.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

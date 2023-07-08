from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database refer to SQLAlchemy
# This video: https://www.youtube.com/watch?v=uZnp21fu8TQ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = "genrey"

# Initialize the database
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))

    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Table model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    posts = db.relationship('Posts', backref='poster')

    def __init__(self, username, password):
        self.username = username
        self.password = password

# This is how we create the database
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index")
def home():
    # Check if the user has really logged in
    if "user" in session:
        user = session["user_id"]
        return render_template("index.html", user=user)

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_password")

        found_user = Users.query.filter_by(username=username).first()

        if password != confirm_pass:
            flash("Inputted passwords does not match", 'error')
            return render_template("register.html")
        elif found_user:
            flash("Username already exists", 'error')
            return render_template("register.html")

        else:
            # Saving data in the table
            # Refer to this video: https://www.youtube.com/watch?v=1nxzOrLWiic
            user = Users(username, password)
            db.session.add(user)
            db.session.commit()

            found_user = Users.query.filter_by(username=username, password=password).first()

            session["user_id"] = found_user.id
            return render_template("index.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        found_user = Users.query.filter_by(username=username, password=password).first()

        if found_user:
            session["user_id"] = found_user.id
            return render_template("index.html")

        else:
            flash("Account does not exist in the database", 'error')
            return render_template("login.html")

    else:
        if "user" in session:
            return redirect("/index")

        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return render_template("index.html")


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        latitude = request.form.get('location')
        longitude = 'test'

        new_post = Posts(latitude = latitude, longitude = longitude, poster_id = session["user_id"])

        db.session.add(new_post)
        db.session.commit()

        return render_template("index.html")







    else:
        return render_template("post.html")


if __name__ == '__main__':
    app.run()

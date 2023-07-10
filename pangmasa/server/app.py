import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Database refer to SQLAlchemy
# This video: https://www.youtube.com/watch?v=uZnp21fu8TQ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = "genrey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
db = SQLAlchemy(app)




class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    image = db.Column(db.String())
    price = db.Column(db.String())
    description = db.Column(db.String())

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
    posts = Posts.query.all()
    return render_template("index.html", posts=posts)

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
            db.session.close()

            found_user = Users.query.filter_by(username=username, password=password).first()

            session["user_id"] = found_user.id
            return redirect("/")

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
            return redirect("/")

        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return redirect("/")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        store_name = request.form.get('store')
        location = request.form.get('location')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        price = request.form.get('price')
        description = request.form.get('description')

        image = request.files['img']

        if image.filename == '':
            flash("Upload an image!")
            return redirect(request.url)

        if image and allowed_file(image.filename):
            filename = secure_filename(str(uuid.uuid1()) + image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = Posts(description=description, store_name=store_name, location=location, latitude=latitude, longitude=longitude, image=filename, price=price, poster_id = session["user_id"])
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")

    else:
        return render_template("post.html")


if __name__ == '__main__':
    app.run()

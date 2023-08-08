import os
import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
#from models import User, Booking



# globals

# Define number of courts to be flexible. For later use.
number_of_courts = 4

# Create a list of courts based on the number of courts
courtlist = [i for i in range(1, number_of_courts+1)]


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
app.config["DEBUG"] = True



# Create a connection cursor
db = SQLAlchemy(app)
#db.init_app(app)

# Create classes for database models

# Class for our users
class User(db.Model):
    __tablename__ = "users"

    id           = db.Column(db.Integer,
                             db.Sequence("users_id_seq"),
                             primary_key=True)
    email       = db.Column(db.String(62) ,
                             nullable=False, unique=True)
    first_name = db.Column(db.String(32) ,
                             nullable=False)
    last_name = db.Column(db.String(32) ,
                             nullable=False)
    street_name = db.Column(db.String(64) ,
                             nullable=False)
    street_number = db.Column(db.String(16) ,
                             nullable=False)
    zip = db.Column(db.String(5) ,
                             nullable=False)
    city = db.Column(db.String(64) ,
                             nullable=False)
    gender = db.Column(db.String(6) ,
                             nullable=False)
    user_since = db.Column(db.DateTime ,
                             nullable=False)
    is_admin = db.Column(db.Boolean ,
                             nullable=False)
    is_confirmed = db.Column(db.Boolean ,
                             nullable=False)
    hash = db.Column(db.String(256) ,
                             nullable=False)

    def __init__(
        self, email, first_name, last_name, street_name, street_number, zip, city, gender, user_since, hash, is_admin=False, is_confirmed=False
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.street_name = street_name
        self.street_number = street_number
        self.zip = zip
        self.city = city
        self.gender = gender
        self.user_since = user_since
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.hash = hash


    def __repr__(self):
        return '<User %r>' % self.email


# Class for our bookings
class Booking(db.Model):
    __tablename__ = "bookings"

    id           = db.Column(db.Integer,
                             db.Sequence("bookings_id_seq"),
                             primary_key=True)
    email       = db.Column(db.String(62) ,
                             nullable=False,)
    court       = db.Column(db.Integer ,
                             nullable=False)
    date        = db.Column(db.Date ,
                             nullable=False)
    start       = db.Column(db.DateTime ,
                             nullable=False)
    end         = db.Column(db.DateTime ,
                             nullable=False)


    def __init__(
        self, email, court, date, start, end
    ):
        self.email = email
        self.court = court
        self.date = date
        self.start = start
        self.end = end


    def __repr__(self):
        return f"<Booking: booking_id={self.id}, member={self.email}, court={self.court}, start={self.start}, end={self.end}>"

# Create database tables if they don`t exist yet
with app.app_context():
    db.create_all()




def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            # Check if there is the current user is logged in
            if session["user"]:
                return f(*args, **kwargs)
        # If no user is stored in session we will get a KeyError. In this case we capture it and redirect the user to login
        except KeyError:
            flash("You need to login first")
            return redirect("/login")

    return wrap


@app.route("/booking", methods=["GET", "POST"])
@login_required
def booking():

    # Get actual date for setting the min date in the form
    today = datetime.date.today()

    if request.method == "GET":

        # Render page
        return render_template("booking.html", today=today)

    if request.method == "POST":

        # Get form data
        input_date = request.form["input_date"]
        input_time = request.form["input_time"]
        duration = request.form["duration"]

        # Split input date into separate values to create a datetime conform format
        year, month, day = input_date.split("-")

        # Split the input time into separate values to create a datetime conform format
        hour, minute = input_time.split(":")

        # Format start time as datetime
        start_input = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

        # Split duration time to use hour and min values for timedelta
        hours_duration, minutes_duration = duration.split(":")

        # Format end time as datetime. end time = start time + duration
        end_input = start_input + (datetime.timedelta(hours=int(hours_duration), minutes=int(minutes_duration)))

        # Initialise list of courts as free
        court_status = ["free"] * number_of_courts

        # Iterate over all courts
        for court in courtlist:

            # Query database for already existing bookings for the chosen day
            court_bookings = Booking.query.filter_by(date=input_date, court=court).all()

            # For debugging purposes
            print("court_bookings")
            print(court_bookings)

            # Iterate over all bookings for this day
            for i in range(len(court_bookings)):

                # Check if the desired booking will interfere with the existing bookings for this court
                if not (end_input <= court_bookings[i].start or start_input >= court_bookings[i].end):

                    # As the index starts with 0 and the courtlist is starting at 1, we have to reduce indexnumber by 1 in order to address the correct court
                    court_status[court-1] = "occupied"

                    # Break out of the loop for this court if one booking interferes
                    break

        # For debugging purposes
        print(courtlist)
        print(court_status)

        # Render template with the available courts to choose from. Pass all values to the next form
        return render_template("booking_return.html", today=today, court_status=court_status, input_date_pass=input_date, start_input_pass=start_input, end_input_pass=end_input)


@app.route("/booking_done", methods=["GET", "POST"])
@login_required
def booking_done():

    if request.method == "POST":

        # Get all form data
        court_select = request.form["court_select"]
        input_date = request.form["input_date_pass"]
        start_input = request.form["start_input_pass"]
        end_input = request.form["end_input_pass"]

        # Get current user
        email = session["user"]

        # For debugging purposes
        print(court_select)

        # Store booking in database
        booking = Booking(email=email, court=court_select, date=input_date, start=start_input, end=end_input)
        db.session.add(booking)

        # Save changes to database
        db.session.commit()

        # Generate success message
        flash("Booking successful!")

        # Return user to index
        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("/user/change_password.html")

    if request.method == "POST":

        # Get form input
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Query the user data
        user = User.query.filter(User.email == session["user"]).first()

        # Check if the current password is right
        if not check_password_hash(user.hash, old_password):

            # Generate error message and return user back to the form
            error_message = "Invalid password"
            return render_template("/user/change_password.html", error_message=error_message)

        else:
            # Check if new password and confirmation is same
            if new_password == confirm_password:

                    # Hash the new password and use it as new password
                    new_hash = generate_password_hash(new_password)
                    user.hash = new_hash

                    # Save new hash to database
                    db.session.commit()

                    # Generate success message
                    flash("Password change successful")

                    # Return user to user settings
                    return redirect("/user_settings")

            else:
                # Generate error message and return user back to form
                error_message = "New Password and Confirmation do not match!"
                return render_template("/user/change_password.html", error_message=error_message)


@app.route("/courts", methods=["GET"])
def courts():
    return render_template("courts.html")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", session=session)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        # Get login data from form
        email = request.form["login_email"]
        password = request.form["login_password"]

        # Get matching user id and hashfrom database
        user = User.query.filter_by(email = email).first()
        print(user)
        print(user.hash)

        # Check if the user is in database
        if user is None:
            # Generate error message and return user to login page again
            error_message = "Invalid email"
            return render_template("login.html", error_message=error_message)

        # Check if the password is correct
        elif not check_password_hash(user.hash, password):

            # Generate error message and return user to login page again
            error_message = "Invalid password"
            return render_template("login.html", error_message=error_message)

        # User is validated
        else:

            # STORE SESSION COOKIE
            session["user"] = email

            # For debugging purposes
            print("user logged in")

            # Flash confirmation
            flash("You are now logged in!")
            # Redirect to index
            return redirect("/")


@app.route("/logout")
@login_required
def logout():
    # Clear session information
    session.clear()

    flash("You have been logged out!")

    # Redirect to index
    return redirect("/", )


@app.route("/pricing", methods=["GET"])
def pricing():
    if request.method == "GET":
        return render_template("pricing.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")

    if request.method == "POST":

        # Get user data from registration form
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        gender = request.form["gender"]
        street_name = request.form.get("street_name")
        street_number = request.form.get("street_number")
        zip = request.form.get("zip")
        city = request.form.get("city")
        email = request.form.get("email")
        password = request.form.get("password")
        pw_confirmation = request.form.get("pw_confirmation")

        # Check if all fields are supplied
        if not first_name or not last_name or not gender or not street_name or not street_number or not zip or not city or not email or not password or not pw_confirmation:
            error_message = "All fields are required"
            return render_template("register.html", error_message=error_message,
                                   first_name=first_name,
                                   last_name=last_name,
                                   street_name=street_name,
                                   street_number=street_number,
                                   zip=zip, city=city,
                                   email=email)

        else:
            # Check if both passwords are the same
            if password != pw_confirmation:
                error_message = "Passwort and repeated password are not equal"
                return render_template("register.html", error_message=error_message,
                            first_name=first_name,
                            last_name=last_name,
                            street_name=street_name,
                            street_number=street_number,
                            zip=zip, city=city,
                            email=email)

            else:
                # Get already registered users with same email from database
                user = User.query.filter_by(email = email).first()
                print(user)
                print(type(user))

                # Check if email already exists
                if user:

                    # Create error message for duplicate email
                    error_message = "Email already registered"

                    # Return error message as alert in new rendered template
                    return render_template("register.html", error_message=error_message,
                            first_name=first_name,
                            last_name=last_name,
                            street_name=street_name,
                            street_number=street_number,
                            zip=zip, city=city,
                            email=email)

                else:
                    # Get timestamp for user creation
                    timestamp = datetime.datetime.now()

                    # Hash the plaintext user password
                    hash = generate_password_hash(password)

                    # Create user object for storing it in database
                    user = User(email=email, first_name=first_name, last_name=last_name, street_name=street_name, street_number=street_number, zip=zip, city=city, gender=gender, user_since=timestamp, hash=hash)

                    # Store userdata in database
                    db.session.add(user)

                    # Save changes to database
                    db.session.commit()

                    # Flash a confirmation and redirect user to index
                    flash('Member registration successful', 'success')

                    return redirect("/")


@app.route("/user_settings", methods=["GET", "POST"])
@login_required
def user_settings():

    if request.method == "GET":

        # Query all bookings from current user and render them on the settings page
        bookings = Booking.query.filter(Booking.email == session["user"]).all()
        return render_template("user_settings.html", bookings=bookings)

    if request.method == "POST":

        # Get booking ID to delete from form
        delete_booking = request.form["delete_booking"]

        # Delete booking ID from database
        booking = Booking.query.filter_by(id=delete_booking).first()
        db.session.delete(booking)

        # Save changes to database
        db.session.commit()

        flash("Booking deleted")

        # Get the remaining bookings and render page again
        bookings = Booking.query.filter(Booking.email == session["user"]).all()

        return render_template("user_settings.html", bookings=bookings)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

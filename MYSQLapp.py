import os

from itsdangerous import URLSafeTimedSerializer
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from flask_modals import Modal
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

import datetime
import pytz
import sqlite3

# globals
courtlist = [1, 2, 3, 4]


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


app.config['MYSQL_HOST'] = 'fiz.mysql.eu.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'fiz'
app.config['MYSQL_PASSWORD'] = 'SecretSaucedChicken1403'
app.config['MYSQL_DB'] = 'fiz$tennis_mysql'

mysql = MySQL(app)

#modal = Modal(app)

#Creating a connection cursor
db = mysql.connection.cursor()


# Set up sqlite database connection
#connection = sqlite3.connect("/home/fiz/tennis-flask/tennis.db", check_same_thread=False)
#db = connection.cursor()

# Function for rounding to the next 30 min. For later use
def ceil_dt(dt, delta):
    return dt + (datetime.datetime.min - dt) % delta



#def login_required(f):
#    @wraps(f)
#    def wrapper(*args, **kwargs):
#        user_id = session.get("user_id")
#        if user_id:
#            user = database.get(user_id)
#            if user:
#                # Success!
#                return f(*args, **kwargs)
#            else:
#                flash("Session exists, but user does not exist (anymore)")
#                return redirect(url_for('login'))
#        else:
#            flash("Please log in")
#            return redirect(url_for('login'))


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)


@app.route("/confirm/<token>")
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    #user = User.query.filter_by(email=email).first_or_404()
    user, is_confirmed = db.execute(''' SELECT email, is_confirmed FROM users WHERE email = ? ''', (email,)).fetchone()
    print(user)
    if is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        is_confirmed = True
        db.execute(''' INSERT INTO users (is_confirmed) VALUES (?) ''', is_confirmed)
        mysql.connection.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect("/")



@app.route("/booking_done", methods=["GET", "POST"])
def booking_done():
    if request.method == "POST":
        court_select = request.form["court_select"]
        input_date = request.form["input_date_pass"]
        start_input = request.form["start_input_pass"]
        end_input = request.form["end_input_pass"]
        email = session["user"]
        print(court_select)

        # Store booking in database
        db.execute(''' INSERT INTO bookings (email, court, date, start, end) VALUES (?, ?, ?, ?, ?) ''', (email, court_select, input_date, start_input, end_input))

        # Save changes to database
        mysql.connection.commit()

        return redirect("/")



@app.route("/booking", methods=["GET", "POST"])
def booking():

    # Get actual date
    #now = ceil_dt(now, datetime.timedelta(minutes=30))
    today = datetime.date.today()

    if request.method == "GET":
        return render_template("booking.html", today=today)


    if request.method == "POST":

        input_date = request.form["input_date"]
        input_time = request.form["input_time"]
        duration = request.form["duration"]
        print("input_date: ", input_date)
        print("input_time: ", input_time)
        print("duration: ", duration)


        year, month, day = input_date.split("-")

        hour, minute = input_time.split(":")
        start_input = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        print("start_input: ", start_input)
        hours_duration, minutes_duration = duration.split(":")
        end_input = start_input + (datetime.timedelta(hours=int(hours_duration), minutes=int(minutes_duration)))
        print("end_input: ", end_input)

        court_status = ["free", "free", "free", "free"]

        for court in courtlist:
            court_bookings = db.execute(''' SELECT start, end FROM bookings WHERE date = ? AND court = ? ''', (input_date, court)).fetchall()

            for i in range(len(court_bookings)):
                start_stored, end_stored = court_bookings[i]
                start_stored = datetime.datetime.strptime(start_stored, "%Y-%m-%d %H:%M:%S")
                end_stored = datetime.datetime.strptime(end_stored, "%Y-%m-%d %H:%M:%S")
                print("start_stored: ", start_stored)
                print("end_stored: ", end_stored)
                if not (end_input <= start_stored or start_input >= end_stored):
                    court_status[court] = "occupied"
                    break



        print(courtlist)
        print(court_status)

        return render_template("booking_return.html", today=today, court_status=court_status, input_date_pass=input_date, start_input_pass=start_input, end_input_pass=end_input)


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

        error_message = ""

        # Get matching user id and hashfrom database
        user, hash = db.execute(''' SELECT id, hash FROM users WHERE email = ? ''', (email,)).fetchone()

        # Check if the user is in database
        if user is None:
            error_message = "Invalid email"
            return render_template("login.html", error_message=error_message)

        # Check if the password is correct
        elif not check_password_hash(hash, password):
            error_message = "Invalid password"
            return render_template("login.html", error_message=error_message)

        # All good, user is validated
        else:
            # STORE SESSION COOKIE
            session["user"] = email
            print("user logged in")

            flash("You are now logged in!")
            # Redirect to index
            return redirect("/")



@app.route("/logout")
#@login_required
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
                users = db.execute(''' SELECT id FROM users WHERE email = ? ''', (email,)).fetchone()

                # Check if username already exists
                if users:

                    # Create error message for duplicate username
                    error_message = "Username already exists"

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

                    # Store userdata in database
                    db.execute(''' INSERT INTO users (email, first_name, last_name, street_name, street_number, zip, city, gender, user_since, is_admin, is_confirmed, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (email, first_name, last_name, street_name, street_number, zip, city, gender, timestamp, False, False, hash))

                    # Save changes to database
                    mysql.connection.commit()

                    # Generate token for email confirmation
                    token = generate_confirmation_token(email)

                    #confirm_url = url_for('confirm_email', token=token, _external=True)
                    #html = render_template('user/activate.html', confirm_url=confirm_url)
                    #subject = "Please confirm your email"
                    #send_email(email, subject, html)



                    flash('A confirmation email has been sent via email.', 'success')




                    #TO DO: Render a success message in a modal to index page as a confirmation for registration
                    return redirect("/")


@app.route("/user_settings", methods=["GET", "POST"])
def user_settings():

    if request.method == "GET":
        bookings = db.execute(''' SELECT id, court, start, end FROM bookings WHERE email = ? ''', (session["user"], )).fetchall()

        return render_template("user_settings.html", bookings=bookings)


    if request.method == "POST":

        if request.form["new_email"]:
            new_email = request.form["new_email"]






        if request.form["delete_booking"]:
            # Get booking ID to delete from form
            delete_booking = request.form["delete_booking"]

            # Delete booking ID from database
            db.execute(''' DELETE FROM bookings WHERE id = ? ''', delete_booking)

            # Save changes to database
            mysql.connection.commit()

            # Get the remaining bookings and render page again
            bookings = db.execute(''' SELECT id, court, start, end FROM bookings WHERE email = ? ''', (session["user"], )).fetchall()

            return render_template("user_settings.html", bookings=bookings)




if __name__ == '__main__':
    app.run(host="0.0.0.0")

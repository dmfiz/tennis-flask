# TENNIS-FLASK
#### Video Demo:  https://youtu.be/wayfbLfjPVQ
#### Description:


# **Overview:**

This project is build as a website for a fictional tennis club.
Users can register themselves and, after successful registration, book available tennis courts for their desired timeslots.

A live demo is currently hosted at https://fiz.eu.pythonanywhere.com


# **Details:**


## Python files:

### **app.py** is the main file where all the flask functions and views are.

### **instance/config.py** holds Flask and database configuration and sensitive data is stored in **.env**.

### **models.py** holds the classes for our database models. Currently not working!
-   When loading the functions from this file there is a database error.
    So the current workaround is to have the classes in our main file.



## Functions, views and helpers:

### **layout.html**
-   This serves as our base template for this web application.

-   Navbar is sticky for better user experience.

-   Navbar items will be displayed depending on if user is logged in or not (for example booking, user settings and logout while logged in and become member and login while logged out).

### **/index.html**
-   This is our main page.

-   has a bootstrap carousel. It currently has no autostart.


### **/register     register.html**
-   HTML form requires all fields before submitting.

-   There is a seperate check in the function for checking if all fields are submitted in order to prevent an error.
    If there is a value missing an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

-   If all fields are submitted the function checks if the inserted password and corresponding confirmation match.
    In case they don`t match, an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

-   After that there is a database query to check if the provided email is not registered yet as the database field for email is unique.
    If the email address is already registered an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

-   When all checks are done we generate a timestamp via datetime.now() for time of user creation.
    This timestamp will be put into database as a value.

-   In order to not store plaintext passwords we need to hash (cipher) the user passsword with a function from werkzeug.security called \generate_password_hash\ .

-   After successfully storing user information in our MySQL database we need to give the user some kind of feedback.
    I tried to work with flashing a confirmation in a bootstrap modal but got into troubles with the layout.
    My solution was to use the Flask Message Flashing function.
    I put a for loop via jinja in all relevant HTML templates. This for loop renders the flashed messages via a dismissable container.
    Exceptions are templates that have a login or register form. Here we insert the error message directly above the submit button.

-   Unfortunately the hosting provider for this project does not support SMTP so I can not set up a email validation for the registration process.


### **/login        login.html**
-   Login function checks the inputted email if this email is registered to one of the users.
    This is done via a database query with the user input.
    If the query returns nothing the input is invalid and user will be prompted with an error message.

-   Next step is a check if the submitted password is correct.
    For this we use the \check_password_hash\ function provided by werkzeug.security.
    If the function returns False we inform the user via error message.

-   After providing the correct email and password we store the current email as the current user in session ( session["user"] ).
    Then we redirect the user to the index ( "/" route) and flash a success message.

### login_required**
-   This is a wrapper function which checks if a user is logged in before it renders the corresponding view.

-   To check the logged-in status we check if session["user"] exists.

-   If session["user"] exists, which means a user is currently logged in, we allow the wrapped function/view.

-   If session["user"] does not exist we will get a KeyError, so we need to try the check and in case of a KeyError we redirect the user to login route and flash a warning.


### **/courts       courts.html**
-   Just lorem ipsum text in combination with some sample pictures. No features implemented here.

-   Provides space to showcase some features of the tennis club.


### **/pricing       pricing.html**
-   Same like /courts we just have some lorem ipsum here to generate some fake content for our website.


### **/user_settings        user_settings.html**
-   Before rendering the page we query the database for all bookings of the currently logged in user.
    The result of that query (list of bookings) is passed to the template and we display each of the bookings inside a row in a table.

-   Right next to each row is a delete button which submits the booking id of that row to our app.
    After deleting the booking from our database we render the remaining bookings again and pass them to the template.

-   On user_settings template there is a link to a separate template where the user could change his/her password.
    I tried to keep both POST forms (change password, delete booking) on one template but I always got errors so I decided to separate them on different templates.

-   In an older version I had a form to change the user`s email address but this led to the problem, that the bookings need to get updated to the new email address.
    Or maybe for assigning the correct user to a booking I have to switch from email address to user ID. Maybe I`ll add this feature in a future version.


### **/change_password      user/change_password.html**
-   This form takes the old password, new password and a confirmation for the new password.

-   Old password is checked via check_password_hash function against the saved hash of the current user.

-   If old password is valid we check if new password and confirmation is equal. If so we update the user password, send the user back to user_settings and flash a confirmation.

-   This file is in a subdirectory (user) as there was the plan to put all the user related htmls (change_email, change_password, confirmation_email, etc.) in a separate directory.


### **/logout**
-   Only visible to users, that are logged in via @login_required wrapper

-   Clears session["user"] and flashes a confirmation message while redirecting user to main route (index.html)





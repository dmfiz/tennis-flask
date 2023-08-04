# TENNIS-FLASK
#### Video Demo:  <URL HERE>
#### Description:
**Overview:**

This project is build as a website for a fictional tennis club.
Users can register themselves and, after successful registration, book available tennis courts for their desired timeslots.


**Details:**


Python files:

**app.py** is the main file where all the flask functions and views are.

**instance/config.py** holds Flask and database configuration and sensitive data is stored in **.env**.



Functions, views and helpers:

**layout.html**
- serves as our base template for this web application.
- Navbar is sticky for better user experience
- Navbar items will be displayed depending on if user is logged in or not

**/  index.html**
- is our main page
- has a bootstrap carousel. It currently has no autostart.


**/register  register.html**
1.  HTML form requires all fields before submitting

2.  There is a seperate check in the function for checking if all fields are submitted in order to prevent an error
    If there is a value missing an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

3.  If all fields are submitted the function checks if the inserted password and corresponding confirmation match.
    In case they don`t match, an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

4.  After that there is a database query to check if the provided email is not registered yet as the database field for email is unique.
    If the email address is already registered an error message will be generated and the user will be returned to the register function.
    This time the input fields will be pre-filled with the already provided values and the aforementioned error message will be displayed.

5.  When all checks are done we generate a timestamp via datetime.now() for time of user creation.
    This timestamp will be put into database as a value.

6.  In order to not store plaintext passwords we need to hash (cipher) the user passsword with a function from werkzeug.security called \generate_password_hash\

7.  After successfully storing user information in our MySQL database we need to give the user some kind of feedback.
    I tried to work with flashing a confirmation in a bootstrap modal but got into troubles with the layout.
    My solution was to use the Flask Message Flashing function.
    I put a for loop via jinja in all relevant HTML templates. This for loop renders the flashed messages via a dismissable container.
    Exceptions are templates that have a login or register form. Here we insert the error message directly above the submit button.


**/login  login.html**
1.  Login function checks the inputted email if this email is registered to one of the users.
    This is done via a database query with the user input.
    If the query returns nothing the input is invalid and user will be prompted with an error message.

2.  Next step is a check if the submitted password is correct.
    For this we use the \check_password_hash\ function provided by werkzeug.security.
    If the function returns False we inform the user via error message.

3.  After providing the correct email and password we store the current email as the current user in session ( session["user"] ).
    Then we redirect the user to the index ( "/" route) and flash a success message.

**/login_required**
-   This is a wrapper function which checks if a user is logged in before it renders the corresponding view

-   To check the logged-in status we check if session["user"] exists.

-   If session["user"] exists, which means a user is currently logged in, we allow the wrapped function/view.

-   If session["user"] does not exist we will get a KeyError, so we need to try the check and in case of a KeyError we redirect the user to login route and flash a warning
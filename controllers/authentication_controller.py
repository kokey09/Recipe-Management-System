from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint
from models.account import Account
from models.account import db
from models.review import Review
from flask_bcrypt import Bcrypt

authentication_controller_bp = Blueprint('authentication_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@authentication_controller_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None  # Define error here

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_email = Account.query.filter_by(email=email).first()
        existing_username = Account.query.filter_by(username=username).first()
        # Check account already exists
        if existing_email:
            error = "An account with this email already exists."
        elif existing_username:
            error = "An account with this username already exists."
        elif password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_account = Account(username=username, email=email, password=hashed_password)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('authentication_controller.login'))
        else:
            error = "Your password and confirm password do not match."

    return render_template('register.html', error=error)


@authentication_controller_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']
        user = Account.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, entered_password):
            if not user.is_deleted:  # Check if the account is not soft deleted
                session['user_id'] = user.id

                if user.type == 'admin':
                    return redirect(url_for('dashboard_controller.dashboard'))
                elif user.type == 'normal':
                    # Query records excluding those with a specific account_id value
                    reviews = Review.query.filter(Review.account_id != -1).all()
                    return redirect(url_for('user_end_controller.user_page'))
            else:
                error = "Account has been soft deleted."
        else:
            error = "Incorrect username or password. Please try again."

    return render_template('login.html', error=error)

@authentication_controller_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the 'user_id' key from the session
    return redirect(url_for('user_end_controller.user_page'))



@authentication_controller_bp.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response

@authentication_controller_bp.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint
from models.account import Account
from models.account import db
from models.review import Review
from flask_bcrypt import Bcrypt


from flask import current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer



authentication_controller_bp = Blueprint('authentication_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()
mail = Mail()

@authentication_controller_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None  # Define notif here
    success = None
    exprired_token = session.pop('exprired_token', None)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_email = Account.query.filter_by(email=email).first()
        existing_username = Account.query.filter_by(username=username).first()
        # Check account already exists
        if len(password) < 8:
            error = "Password must be at least 8 characters long."
        elif existing_username:
            error = "An account with this username already exists."
        elif existing_email:
            error = "An account with this email already exists."
        elif password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                    # Store the account details in the database with a status of 'unverified'
            new_account = Account(username=username, email=email, password=hashed_password, status='unverified')
            db.session.add(new_account)
            db.session.commit()
                    # Generate a verification token and send it to the user's email
            token = generate_verification_token(email)
            send_verification_email(email, token)

            success = f"An email has been sent to {email} with a link to verify your account. Please check your email and click the link to complete your registration"
        else:
            error = "Your password and confirm password do not match."

    return render_template('register.html', error=error, success=success, exprired_token=exprired_token)


@authentication_controller_bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):
    email = confirm_verification_token(token)

    if not email:
        session['exprired_token'] = 'Invalid or expired token'
        return redirect(url_for('authentication_controller.register'))

    # Look up the account in the database and update its status
    account = Account.query.filter_by(email=email).first()
    if account and account.status == 'unverified':
        account.status = 'verified'
        db.session.commit()
        session['success'] = "Account has been registered"
        return redirect(url_for('authentication_controller.login'))

    flash('An error occurred')
    return redirect(url_for('authentication_controller.register'))


def send_verification_email(email, token):
    msg = Message('Account Verification', sender='your-email@gmail.com', recipients=[email])
    verify_url = url_for('authentication_controller.verify_email', token=token, _external=True)
    msg.body = f'Click the following link to verify your account: {verify_url}'
    mail.send(msg)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email)

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            max_age=expiration
        )
    except:
        return False
    return email


@authentication_controller_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        entered_password = request.form.get('password')
        user = Account.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password, entered_password):
            error="Incorrect username or password. Please try again."
            return render_template('login.html', error=error)

        if user.is_deleted:
            error="Account has been soft deleted."
            return render_template('login.html', error=error)

        if user.status != 'verified':
            token = generate_verification_token(user.email)  # Generate a new token
            send_verification_email(user.email, token)  # Send the verification email
            error="Account is not verified. Please check your email for the verification link."
            return render_template('login.html', error=error)

        session['user_id'] = user.id
        if user.type == 'admin':
            return redirect(url_for('dashboard_controller.dashboard'))
        elif user.type == 'normal':
            return redirect(url_for('user_end_controller.user_page'))

    success = session.pop('success', None)
    reset_password = session.pop('reset_password', None)
    return render_template('login.html', success=success, reset_password=reset_password)


@authentication_controller_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the 'user_id' key from the session
    return redirect(url_for('authentication_controller.login'))


@authentication_controller_bp.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@authentication_controller_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    notif = None
    if request.method == 'POST':
        email = request.form.get('email') 
        # looking for the email in the database
        user = Account.query.filter_by(email=email).first()

        if not user:
            notif = "This email does not exist in our database."
        else:
            token = generate_reset_token(email)
            send_reset_email(email, token)
            notif = "An email has been sent to your email address."

    return render_template('/forgot_password.html', notif=notif)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email


def send_reset_email(email, token):
    msg = Message('Password Reset Request', sender='your-email@gmail.com', recipients=[email])
    msg.body = f'Click the following link to reset your password: {url_for("authentication_controller.reset_password", token=token, _external=True)}'
    mail.send(msg)


@authentication_controller_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = confirm_reset_token(token)

        if not email:
            session['reset_password'] = 'Invalid or expired token'
            return redirect(url_for('authentication_controller.login'))

        if len(password) < 8:
            error = 'Password must be at least 8 characters long.'
            return render_template('reset_password.html', token=token, error=error)

        if password != confirm_password:
            error = 'Your password and confirm password do not match.'
            return render_template('reset_password.html', token=token, error=error)

        user = Account.query.filter_by(email=email).first()
        if not user:
            error = 'User not found'
            return redirect(url_for('authentication_controller.login'))
        
        if bcrypt.check_password_hash(user.password, password):
            error = 'New password cannot be the same as the old password.'
            return render_template('reset_password.html', token=token, error=error)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        session['reset_password'] = "Password has been reset."
        return redirect(url_for('authentication_controller.login'))

    return render_template('reset_password.html', token=token, error=error)

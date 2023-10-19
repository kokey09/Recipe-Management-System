from flask import  render_template, request, redirect, url_for, flash, jsonify, session, Blueprint
from models.account import Account
from models.account import db

from flask_bcrypt import Bcrypt

account_controller_bp = Blueprint('account_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@account_controller_bp.route('/accounts')
def accounts():
    accounts_data = Account.query.all()
    return render_template('accounts.html', accounts=accounts_data)

@account_controller_bp.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    account_to_delete = Account.query.get(account_id)
    if account_to_delete:
        db.session.delete(account_to_delete)
        db.session.commit()
    return redirect(url_for('account_controller.accounts'))


@account_controller_bp.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if request.method == 'POST':
        for field in ['username', 'email', 'type']:
            if field in request.form:
                setattr(account, field, request.form[field])

        if 'password' in request.form:
            new_password = request.form['password']
            # Rehash the new password and update it in the database
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            account.password = hashed_password

        db.session.commit()
        return redirect(url_for('account_controller.accounts'))

    return render_template('edit_account.html', account=account)

@account_controller_bp.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
        if user.type == 'admin':
            return render_template('dashboard.html')
        else:
            flash('You do not have access to the dashboard')
            return redirect(url_for('user_page'))
    else:
        flash('Please log in to access the dashboard')
        return redirect(url_for('account_controller.login'))



@account_controller_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']

        user = Account.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, entered_password):
            session['user_id'] = user.id
            flash('Login successful!')

            if user.type == 'admin':
                return redirect(url_for('account_controller.dashboard'))
            elif user.type == 'normal':
                return redirect(url_for('ingredient_controller.user_page'))
        else:
            error = "Incorrect username or password. Please try again."

    return render_template('login.html', error=error)

@account_controller_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the 'user_id' key from the session
        flash('You have been logged out', 'success')
    return redirect(url_for('ingredient_controller.user_page'))


@account_controller_bp.before_request
def check_user_auth():
    if request.endpoint == 'dashboard' and 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))
    elif request.endpoint == 'accounts' and 'user_id' not in session:
        flash('You need to log in first to access accounts.', 'error')
        return redirect(url_for('login'))
    elif request.endpoint == 'ingredients' and 'user_id' not in session:
        flash('You need to log in first to access accounts.', 'error')
        return redirect(url_for('login'))
    elif request.endpoint == 'recipes' and 'user_id' not in session:
        flash('You need to log in first to access accounts.', 'error')
        return redirect(url_for('login'))
    elif request.endpoint == 'recipe_ingredients' and 'user_id' not in session:
        flash('You need to log in first to access accounts.', 'error')
        return redirect(url_for('login'))


@account_controller_bp.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response

@account_controller_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None  # Define error here

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_account = Account(username=username, email=email, password=hashed_password)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('account_controller.login'))
        else:
            error = "Your password and confirm password do not match."

    return render_template('register.html', error=error)

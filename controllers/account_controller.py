from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint
from models.account import Account
from models.account import db
from models.review import Review
from flask_bcrypt import Bcrypt

account_controller_bp = Blueprint('account_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@account_controller_bp.route('/accounts')
def accounts():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            accounts_data = Account.query.all()
            return render_template('accounts.html', accounts=accounts_data, user=user)
        else:
            flash('You do not have permission to access accounts.', 'error')
            return redirect(url_for('ingredient_controller.user_page'))
    else:
        flash('Please log in to access accounts.', 'error')
        return redirect(url_for('account_controller.login'))

@account_controller_bp.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    if request.method == 'POST':
        account_to_delete = Account.query.get(account_id)
        if account_to_delete:
            try:
                # Soft delete the account
                account_to_delete.is_deleted = True
                db.session.commit()
                flash('Account deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while soft deleting the account: ' + str(e), 'error')
        else:
            flash('Account not found', 'error')
    return redirect(url_for('account_controller.accounts'))



@account_controller_bp.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if request.method == 'POST':
        for field in ['username', 'email', 'type', 'is_deleted']:
            if field in request.form:
                setattr(account, field, request.form[field])

        is_deleted = request.form.get('is_deleted', '0') == '1'
        account.is_deleted = is_deleted

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

        if user and user.type == 'admin':
            return render_template('dashboard.html', user=user)
        else:
            return redirect(url_for('ingredient_controller.user_page'))

    else:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('account_controller.login'))



@account_controller_bp.route('/login', methods=['GET', 'POST'])
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
                    return redirect(url_for('account_controller.dashboard'))
                elif user.type == 'normal':
                    # Query records excluding those with a specific account_id value
                    reviews = Review.query.filter(Review.account_id != -1).all()
                    return redirect(url_for('ingredient_controller.user_page'))

            error = "Account has been soft deleted."
        else:
            error = "Incorrect username or password. Please try again."

    return render_template('login.html', error=error)




@account_controller_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the 'user_id' key from the session
    return redirect(url_for('ingredient_controller.user_page'))


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
            return redirect(url_for('account_controller.login'))
        else:
            error = "Your password and confirm password do not match."

    return render_template('register.html', error=error)




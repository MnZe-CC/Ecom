from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_user import AdminUser, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Find user
        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            # Set session
            session['admin_id'] = user.id
            session['admin_username'] = user.username
            session['is_admin'] = True

            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('admin/login.html')

@auth_bp.route('/logout')
def logout():
    """Admin logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
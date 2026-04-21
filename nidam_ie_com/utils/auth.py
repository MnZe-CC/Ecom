from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    """
    Decorator to require login for admin routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    """
    Decorator to ensure only admins can access certain routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session or not session.get('is_admin', False):
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated_function
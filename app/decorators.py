from functools import wraps

from flask import abort
from flask_login import current_user

from .models import Permission, Role, AnonymousUser


def permission_required(permission):
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def user_has_role(role_id):
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_anonymous or current_user.role_id != role_id:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def company_required(f):
    return user_has_role(Role.COMPANY_ID)(f)


def user_required(f):
    return user_has_role(Role.USER_ID)(f)

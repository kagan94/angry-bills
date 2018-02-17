from flask import url_for


def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(index_for_role)


def index_for_role(role):
    return url_for(role.index)


def allowed_file(filename):
    allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_user_file(f):
    from werkzeug.utils import secure_filename
    from flask import current_app
    from flask.ext.login import current_user
    import os.path

    f_name = secure_filename(f.filename)
    tgt_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
    if not os.path.exists(tgt_folder):
        os.makedirs(tgt_folder)

    f_path = os.path.join(tgt_folder, f_name)
    f.save(f_path)
    return f_name

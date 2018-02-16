from flask import render_template
# from ..models import EditableHTML

from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    # editable_html_obj = EditableHTML.get_editable_html('about')
    # return render_template('main/about.html', editable_html_obj=editable_html_obj)
    return render_template('main/about.html')


@main.route('/expense/add')
def add_expense():
    # TODO: Handle adding expense to the database
    return render_template('main/expense/add.html')

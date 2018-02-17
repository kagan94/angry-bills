from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
# from ..models import EditableHTML
from flask import request
import datetime

from flask import url_for
from flask.ext.login import current_user
from flask_login import login_required

from app.utils import save_user_file
from .forms import AddExpenseForm
from seb_api import SebApi
from . import main
from .. import db
from ..models import Expense, ExpenseType


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    # editable_html_obj = EditableHTML.get_editable_html('about')
    # return render_template('main/about.html', editable_html_obj=editable_html_obj)
    return render_template('main/about.html')


@login_required
@main.route('/expense/add', methods=['GET', 'POST'])
def add_expense():
    form = AddExpenseForm()

    if request.method == 'POST':
        f = request.form
        photo = request.files['photo']
        expense, is_form_valid = Expense(), True

        if photo.filename:
            filename = save_user_file(photo)
            expense.photo = filename
        else:
            is_form_valid = False

        if is_form_valid:
            expense.user_id = current_user.id
            expense.expense_type_id = ExpenseType.findByTag(f["expense_type"])
            expense.comments = f['comments']
            expense.seb_payment_date = f['seb_payment_date']
            expense.seb_endToEndId = f['seb_endToEndId']
            expense.seb_transactionAmount = f['seb_transactionAmount']
            expense.seb_transactionCurrency = f['seb_transactionCurrency']
            expense.seb_counterPartyAccount = f['seb_counterPartyAccount']
            expense.seb_unstructuredReference = f['seb_unstructuredReference']
            expense.seb_structuredReference = f['seb_structuredReference']
            expense.seb_counterPartyName = f['seb_counterPartyName']
            db.session.add(expense)
            db.session.commit()

            flash('Your expense was successfully added', 'success')
            return redirect(url_for('main.add_expense'))
        else:
            flash('Invalid file or form data', 'form-error')
    transactions = SebApi().get_payments(10)
    return render_template('main/expense/add.html', **locals())


@main.route('/expenses', methods=['GET'])
def all_expenses():
    form = None
    # form = ConfirmForm()
    # if request.method == 'POST':
    #     pass
    return render_template('main/expense/all.html', **locals())

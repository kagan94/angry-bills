from flask import current_app
from flask import flash
from flask import render_template
from flask import request
# from ..models import EditableHTML
from flask import request
import datetime

from flask.ext.login import login_required

from app.utils import save_user_file
from .forms import ConfirmForm, AddExpenseForm
from seb_api import SebApi
from . import main
from .. import db
from ..models import Expense


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
        expense, is_form_valid = Expense(), True

        f = request.files['photo']
        if f.filename:
            filename = save_user_file(f)
            expense.photo = filename
        else:
            is_form_valid = False

        if is_form_valid:
            db.session.add(expense)
            db.session.commit()

            flash('Your expense was successfully added', 'success')
        else:
            flash('Invalid file or form data', 'form-error')
    transactions = SebApi().get_payments(10)
    return render_template('main/expense/add.html', **locals())


@main.route('/expense/confirm', methods=['GET', 'POST'])
def confirm_expense():
    form = ConfirmForm()
    if request.method == 'POST':
        paymentId = request.form["paymentID"]
        reciever = request.form["reciever"]
        recievedAmount = request.form["amount"]
        paymentDate = datetime.date(*map(int, request.form["paymentDate"].split('-')))
        expenseType = request.form["expenseType"]
        paymentDescription = request.form["description"]

        new_expense = Expense(id=paymentId,
                              creditor=reciever,
                              amount=recievedAmount,
                              date=paymentDate,
                              expense_type_id=expenseType,
                              expense_description=paymentDescription)
        db.session.add(new_expense)
        db.session.commit()
    return render_template('main/expense/confirm.html', **locals())

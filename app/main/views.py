from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
# from ..models import EditableHTML
from flask import request
import datetime

from flask import url_for
from flask_login import login_required, current_user

from app.decorators import user_required, company_required
from app.utils import save_user_file
from .forms import AddExpenseForm
from seb_api import SebApi
from . import main
from .. import db
from ..models import Expense, ExpenseType, User, Role


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    # editable_html_obj = EditableHTML.get_editable_html('about')
    # return render_template('main/about.html', editable_html_obj=editable_html_obj)
    return render_template('main/about.html')


@main.route('/expense/add', methods=['GET', 'POST'])
@user_required
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
            expense.amount = f['amount']
            expense.expense_type_id = ExpenseType.findByTag(f["expense_type"])
            expense.comments = f['comments']
            expense.seb_payment_date = f['seb_payment_date']
            expense.seb_endToEndId = f['seb_endToEndId']
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
@user_required
def all_expenses():
    form = None
    # form = ConfirmForm()
    # if request.method == 'POST':
    #     pass
    return render_template('main/expense/all.html', **locals())


@main.route('/requests', methods=['GET', 'POST'])
@company_required
def all_requests():
    expenses = Expense.query\
        .filter_by(is_rejected=False)\
        .filter(Expense.user.has(company_id=current_user.id))\
        .all()
    employees = User.query.filter_by(company_id=current_user.id, role_id=Role.USER_ID).all()

    return render_template('main/request/all.html', **locals())


@main.route('/expense/<id>/reject', methods=['POST'])
@company_required
def reject_expense(id):
    expense = Expense.query\
        .filter_by(id=int(id), is_rejected=False)\
        .filter(Expense.user.has(company_id=current_user.id))\
        .first_or_404()
    expense.is_rejected = True
    db.session.add(expense)
    db.session.commit()

    flash('Your changes have been saved', 'success')
    return redirect(url_for('main.all_requests'))


@main.route('/expense/<id>/accept', methods=['POST'])
@company_required
def accept_expense(id):
    # TODO: Request to make refund here...

    expense = Expense.query\
        .filter_by(id=int(id), is_rejected=False)\
        .filter(Expense.user.has(company_id=current_user.id))\
        .first_or_404()
    expense.is_approved = True
    db.session.add(expense)
    db.session.commit()

    flash('Your changes have been saved', 'success')
    return redirect(url_for('main.all_requests'))

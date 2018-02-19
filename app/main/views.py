from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user

from app.decorators import user_required, company_required
from app.utils import save_user_file
from seb_api import SebApi
from . import main
from .forms import AddExpenseForm
from .. import db
from ..models import Expense, ExpenseType, User, Role


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
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
            expense.amount = float(f['amount'])
            expense.expense_type_id = ExpenseType.findByTag(f["expense_type"])
            expense.comments = f['comments']
            expense.seb_payment_date = f['seb_payment_date']
            expense.seb_endToEndId = f['seb_endToEndId']
            expense.seb_transactionCurrency = f['seb_transactionCurrency']
            expense.seb_counterPartyAccount = f['seb_counterPartyAccount']
            expense.seb_unstructuredReference = f['seb_unstructuredReference']
            expense.seb_structuredReference = f['seb_structuredReference']
            expense.seb_counterPartyName = f['seb_counterPartyName']
            # expense = Expense.query \
            #     .filter_by(id=int(expense_id), is_rejected=False) \
            #     .filter(Expense.user.has(company_id=current_user.id)) \
            #     .first_or_404()

            comment = 'Payment date: %s. Description: %s. Struct.ref.: %s. Counter party name: %s' \
                      % (expense.seb_payment_date, expense.seb_unstructuredReference, expense.seb_structuredReference,
                         expense.seb_counterPartyName)

            # Request to make refund here...
            seb_api = SebApi()
            accounts = seb_api.get_accounts()
            sender_iban = seb_api.find_iban(accounts, expense.amount)
            if not sender_iban:
                flash('Not enough money on any of SEB accounts', 'form-error')
                return redirect(url_for('main.add_expense'))

            resp = seb_api.create_payment(debtorAccount=sender_iban,
                                          amount=expense.amount,
                                          creditorAccount=expense.seb_counterPartyAccount,
                                          endToEndPoint=expense.seb_endToEndId,
                                          currency=expense.seb_transactionCurrency,
                                          creditor='',
                                          debtor='',
                                          commentUnstructured=comment)
            if not resp:
                flash('SEB create payment transaction failed', 'form-error')
                return redirect(url_for('main.add_expense'))
            expense.is_paid = True
            expense.is_approved = True

            # Save expense
            db.session.add(expense)
            db.session.commit()

            flash('Your expense was successfully refunded', 'success')
            return redirect(url_for('main.all_expenses'))
        else:
            flash('Invalid file or form data', 'form-error')

    transactions = SebApi().get_payments(size=5)
    return render_template('main/expense/add.html', **locals())


@main.route('/expenses', methods=['GET'])
@user_required
def all_expenses():
    expenses = Expense.query.filter(Expense.user_id == current_user.id).all()
    return render_template('main/expense/all.html', **locals())


@main.route('/requests', methods=['GET'])
@company_required
def all_requests():
    expenses_q = Expense.query.filter(Expense.user.has(company_id=current_user.id))

    refund_status = request.args.get('refund_status')
    if refund_status == 'paid':
        expenses_q = expenses_q.filter_by(is_approved=True, is_paid=True)
    elif refund_status == 'approved':
        expenses_q = expenses_q.filter_by(is_approved=True)
    elif refund_status == 'rejected':
        expenses_q = expenses_q.filter_by(is_rejected=True)
    else:
        expenses_q = expenses_q.filter_by(is_approved=False, is_rejected=False)

    employees_ids_str, employees_ids = request.args.get('employees_ids'), {}
    if employees_ids_str:
        employees_ids = {int(employee_id): int(employee_id) for employee_id in employees_ids_str.split(',')}
        expenses_q = expenses_q.filter(Expense.user_id.in_(employees_ids.keys()))

    expenses = expenses_q.all()
    employees = User.query.filter_by(company_id=current_user.id, role_id=Role.USER_ID).all()

    return render_template('main/request/all.html', **locals())


@main.route('/expense/<expense_id>/reject', methods=['POST'])
@company_required
def reject_expense(expense_id):
    expense = Expense.query \
        .filter_by(id=int(expense_id), is_rejected=False) \
        .filter(Expense.user.has(company_id=current_user.id)) \
        .first_or_404()
    expense.is_rejected = True
    db.session.add(expense)
    db.session.commit()

    flash('Your changes have been saved', 'success')
    return redirect(url_for('main.all_requests'))


# @main.route('/expense/<expense_id>/accept', methods=['POST'])
# @company_required
# def accept_expense(expense_id):
#     pass

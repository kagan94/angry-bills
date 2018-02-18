#!/usr/bin/env python
import os
import random
import subprocess

import copy

from config import Config

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from redis import Redis
from rq import Connection, Queue, Worker

from app import create_app, db
from app.models import Role, User, ExpenseType, IntegrityError, Expense, choice

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.before_first_request
def create_database():
    db.create_all()


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_users(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    recreate_db()
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    print('Added Roles')

    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                full_name='Admin Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()

    add_fake_users(number_users=10)

    # Add test Company
    company_user = User(full_name="Company Test", email='company@test.com', password='test123', role_id=Role.COMPANY_ID)
    db.session.add(company_user)
    db.session.commit()

    # Add test User
    test_user = User(full_name="Test User", email='test@test.com', password='test123', role_id=Role.USER_ID, company_id=company_user.id)
    db.session.add(test_user)
    db.session.commit()

    print('Added Users')

    # ExpenseType
    expense_types = [
        [ExpenseType.TRANSPORT_ID, 'Transport'],
        [ExpenseType.MEAL_ID, 'Meal'],
        [ExpenseType.ACCOMMODATION_ID, 'Accommodation'],
        [ExpenseType.CORPORATE_ID, 'Corporate']]
    for record in expense_types:
        exp_type = ExpenseType.query.filter_by(id=record[0]).first()
        if not exp_type:
            exp_type = ExpenseType(id=record[0], name=record[1])
            db.session.add(exp_type)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    print('Added ExpenseTypes')

    # Add test Expenses to test user
    expense_types = ExpenseType.query.all()
    for i in range(1, 11):
        is_approved = bool(random.getrandbits(1))
        is_paid = bool(random.getrandbits(1)) if is_approved else False
        dummy_expense = Expense(comments='Dummy test instance', amount=(150 * i**2), is_approved=is_approved, is_paid=is_paid,
                                seb_payment_date='2018-02-18',
                                seb_endToEndId='random__str',
                                seb_transactionCurrency='EUR',
                                seb_counterPartyAccount='xxxxxxxxx',
                                seb_structuredReference='xxxxxxxxx',
                                seb_unstructuredReference='xxxxxxxxx',
                                seb_counterPartyName='xxxxxxxxx',
                                user_id=test_user.id,
                                expense_type=choice(expense_types))
        db.session.add(dummy_expense)
    db.session.commit()
    print('Added Expenses')


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(
        host=app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()

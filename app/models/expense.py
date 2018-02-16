import datetime

from .. import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    is_confirmed = db.Column(db.Boolean, default=True)
    amount = db.Column(db.DECIMAL)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # description = db.Column(db.String(500))
    # due_date = db.Column(db.DATE)
    # updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'))

    # define relationships
    user = db.relationship('User', backref='expenses')
    expense_type = db.relationship('ExpenseType', backref='expenses')

    def __repr__(self):
        return 'ID: %s, user_id: %s, name: %s, amount: %.2f, remaining amount: %.2f'\
               % (self.id, self.user_id, self.name, self.amount, self.remaining_amount)

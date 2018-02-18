import datetime

from .. import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(500))
    amount = db.Column(db.FLOAT)
    is_rejected = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    seb_payment_date = db.Column(db.DATE)
    seb_endToEndId = db.Column(db.String(200))
    seb_transactionCurrency = db.Column(db.String(10))
    seb_counterPartyAccount = db.Column(db.String(200))
    seb_unstructuredReference = db.Column(db.String(200))
    seb_structuredReference = db.Column(db.String(200))
    seb_counterPartyName = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'))

    # define relationships
    user = db.relationship('User', backref='expenses')
    expense_type = db.relationship('ExpenseType', backref='expenses')

    def __repr__(self):
        return 'ID: %s, user_id: %s, amount: %.2f' % (self.id, self.user_id, self.amount)

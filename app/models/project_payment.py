from .. import db


class ProjectPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)
    is_paid = db.Column(db.Boolean, default=False)
    paid_at = db.Column(db.DateTime)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # define relationships
    user = db.relationship('User', backref='payments')
    project = db.relationship('Project', backref='payments')

    def __repr__(self):
        return 'ID: %s, project ID: %s, amount: %.2f, isPaid: %s' \
               % (self.id, self.project_id, self.amount, self.is_paid)

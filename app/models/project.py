import datetime

from .. import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    amount = db.Column(db.DECIMAL)
    remaining_amount = db.Column(db.DECIMAL)
    due_date = db.Column(db.DATE)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_type_id = db.Column(db.Integer, db.ForeignKey('project_type.id'))

    # define relationships
    user = db.relationship('User', backref='projects')
    project_type = db.relationship('ProjectType', backref='projects')

    def __repr__(self):
        return 'ID: %s, user_id: %s, name: %s, amount: %.2f, remaining amount: %.2f'\
               % (self.id, self.user_id, self.name, self.amount, self.remaining_amount)

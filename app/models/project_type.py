from .. import db


class ProjectType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return 'ID: %s, name: %s' % (self.id, self.name)

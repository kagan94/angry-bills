from .. import db


class ExpenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    TRANSPORT_ID = 1
    MEAL_ID = 2
    ACCOMMODATION_ID = 3
    CORPORATE_ID = 4

    def __repr__(self):
        return 'ID: %s, name: %s' % (self.id, self.name)

    @staticmethod
    def findByTag(tag):
        if tag == 'transport':
            return ExpenseType.TRANSPORT_ID
        elif tag == 'meal':
            return ExpenseType.MEAL_ID
        elif tag == 'accommodation':
            return ExpenseType.ACCOMMODATION_ID
        elif tag == 'corporate':
            return ExpenseType.CORPORATE_ID

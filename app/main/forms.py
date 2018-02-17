from wtforms import Form, StringField


class AddExpenseForm(Form):
    test = StringField('Test')

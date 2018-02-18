from random import seed, choice

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # Consts
    USER_ID = 1
    COMPANY_ID = 2
    ADMIN_ID = 3

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Company': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(1))  # todo: remove later..
    last_name = db.Column(db.String(1))  # todo: remove later..
    full_name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    seb_token = db.Column(db.String(200), unique=True, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # define relationships
    company = db.relation('User', remote_side=[id])
    # company = db.relationship('User', backref='employees')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=Permission.ADMINISTER).first()
            if self.role_id is None:
                self.role_id = Role.USER_ID

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def is_user(self):
        return self.role_id == Role.USER_ID

    def is_company(self):
        return self.role_id == Role.COMPANY_ID

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()
        companies = ['Google', 'Fortumo', 'Mooncascade', 'Ciclum', 'Facebook']

        seed()
        for i in range(count):
            full_name = ('%s %s' % (fake.first_name(), fake.last_name()))
            rand_role = choice(roles)

            if rand_role.id == Role.COMPANY_ID:
                full_name = choice(companies)

            u = User(
                full_name=full_name,
                email=fake.email(),
                password='password',
                confirmed=True,
                role=rand_role,
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return self.full_name


class UserQuery:
    @staticmethod
    def companies():
        return User.query.filter_by(role_id=Role.COMPANY_ID)


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


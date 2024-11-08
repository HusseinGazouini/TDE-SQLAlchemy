from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    # Flask-Login required methods (UserMixin already includes these, but you can override them if needed)
    @property
    def is_active(self):
        return True  # You can add your own logic to control whether the user is active

    @property
    def is_authenticated(self):
        return True  # If the user is logged in, they are authenticated

    @property
    def is_anonymous(self):
        return False  # If the user is logged in, they are not anonymous

    def __repr__(self):
        return f'<User {self.username}>'

class Person(db.Model):
    __tablename__ = 'estudantes'

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)
    job = db.Column(db.Text)

    def __repr__(self):
        return f'Person with name {self.name} and age {self.age}'

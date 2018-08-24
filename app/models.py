from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):

    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), index=True, unique=True)
    username=db.Column(db.String(100), index=True, unique=True)
    password_hash=db.Column(db.String(128))
    
    def __init__(self, email, username, password_hash):
        self.email=email
        self.username=username
        self.password_hash=password_hash

    def __repr__(self):
        return '<User: Username {0}, Email {1}'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):

    __tablename__='books'

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    author=db.Column(db.String(50))
    category=db.Column(db.String(50))
    added_on=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    done=db.Column(db.Boolean, default=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, title, author, category, added_on, done):
        self.title=title
        self.author=author
        self.category=category
        self.added_on=added_on
        self.done=done

    def __repr__(self):
        return '<Book: Title - {0}, Author - {1}, Category - {2}, Added On: {3}, Done - {4} >'.format(self.title, self.author, self.category, self.added_on, self.done)

# class Category(db.Model):

#     __tablename__='categories'

#     id=db.Column(db.Integer, primary_key=True)
#     category=db.Column(db.String(20))
#     book_id=db.Column(db.Integer, db.ForeignKey('books.id'))

#     def __repr__(self):
#         return '<Category: {0}>'.format(self.category)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
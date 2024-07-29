from applications.database import db
from flask_security import UserMixin, RoleMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(500), nullable=False, unique=True)  # Changed to 'username' for consistency
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True)

    owned_books = db.relationship('OwnedBooks', backref='user', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Requests', backref='user', lazy=True, cascade="all, delete-orphan")
    borrowed_books = db.relationship('BorrowedBooks', backref='user', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedbacks', backref='user', lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'  # Corrected to use 'username'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'


class RoleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    borrowed_books = db.relationship('BorrowedBooks', backref='admin', lazy=True)


class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(500), nullable=False)

    books = db.relationship('Books', backref='section', lazy=True, cascade="all, delete-orphan")


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn_no = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500))
    date_published = db.Column(db.Date, nullable=True)

    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    owned_books = db.relationship('OwnedBooks', backref='books', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Requests', backref='books', lazy=True, cascade="all, delete-orphan")
    borrowed_books = db.relationship('BorrowedBooks', backref='books', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedbacks', backref='books', lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship('Transaction', backref='books', lazy=True, cascade="all, delete-orphan")


class OwnedBooks(db.Model):
    __tablename__ = 'ownedbooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_purchase = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requested_days = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


class BorrowedBooks(db.Model):
    __tablename__ = 'borrowedbooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    approved_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)


class Feedbacks(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedback = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

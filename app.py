import os
from flask import Flask, redirect, render_template, request, url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from datetime import date, datetime,timedelta

from sqlalchemy import  create_engine, desc, func, text

current_dir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(current_dir, 'database.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SQLALCHEMY_ECHO'] = True  # Add this line for debugging output
app.secret_key = 'secret_key'


db = SQLAlchemy(app)
app.app_context().push()


#----------------------------------------------------------------

class User(db.Model):
    __tablename__='user'
    UserID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    UserName = db.Column(db.String(500), nullable =False)
    Email =  db.Column(db.String(500), nullable =False)
    Password = db.Column(db.String(500), nullable =False)

    OwnedBooksR=db.relationship('OwnedBooks',backref='user',lazy=True,cascade="all, delete-orphan")
    RequestsR=db.relationship('Requests',backref='user',lazy=True,cascade="all, delete-orphan")
    BorrowedBooksR=db.relationship('BorrowedBooks',backref='user',lazy=True,cascade="all, delete-orphan")
    FeedbacksR=db.relationship('Feedbacks',backref='user',lazy=True,cascade="all, delete-orphan")
    TransactionsR=db.relationship('Transaction',backref='user',lazy=True,cascade="all, delete-orphan")

class Admin(db.Model):
    __tablename__='admin'
    AdminID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    AdminName = db.Column(db.String(500), nullable =False)
    Email =  db.Column(db.String(500), nullable =False,unique = True)
    Password = db.Column(db.String(500), nullable =False)


    BorrowedBooksR=db.relationship('BorrowedBooks',backref='Admin',lazy=True)


class Section(db.Model):
    __tablename__='section'
    SectionID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    Genre=db.Column(db.String(500), nullable =False)


    BookR = db.relationship('Books',backref='section',lazy=True,cascade="all, delete-orphan")

class Books(db.Model):
    __tablename__='books'
    BookID = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    ISBNno = db.Column(db.Integer(), nullable =False)
    Author = db.Column(db.String(500), nullable =False)
    Price = db.Column(db.Integer(), nullable =False)
    Name=db.Column(db.String(500), nullable =False)
    Description = db.Column(db.String(500))
    DatePublished = db.Column(db.Date(),nullable =True)
    
    SectionID = db.Column(db.Integer,db.ForeignKey('section.SectionID'),nullable =False)

    OwnedBooksR=db.relationship('OwnedBooks',backref='books',lazy=True,cascade="all, delete-orphan")
    RequestsR=db.relationship('Requests',backref='books',lazy=True,cascade="all, delete-orphan")
    BorrowedBooksR=db.relationship('BorrowedBooks',backref='books',lazy=True,cascade="all, delete-orphan")
    FeedBacksR=db.relationship('Feedbacks',backref='books',lazy=True,cascade="all, delete-orphan")
    TransactionR=db.relationship('Transaction',backref='books',lazy=True,cascade="all, delete-orphan")

class OwnedBooks(db.Model):
    __tablename__='ownedbooks'
    PurchaseID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    DateOfPurchase = db.Column(db.Date(),nullable=False)

    UserID=db.Column(db.Integer,db.ForeignKey('user.UserID'),nullable =False)
    BookId=db.Column(db.Integer,db.ForeignKey('books.BookID'),nullable =False)

class Requests(db.Model):
    __tablename__='requests'
    RequestID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    RequestedDays = db.Column(db.Integer,nullable=False)
    DateOfIssue=db.Column(db.Date(),nullable=False)

    UserID=db.Column(db.Integer,db.ForeignKey('user.UserID'),nullable =False)
    BookId=db.Column(db.Integer,db.ForeignKey('books.BookID'),nullable =False)

class BorrowedBooks(db.Model):
    __tablename__='borrowedbooks'
    ID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    From=db.Column(db.Date(),nullable=False)
    To=db.Column(db.Date(),nullable=False)

    UserID=db.Column(db.Integer,db.ForeignKey('user.UserID'),nullable =False)
    BookId=db.Column(db.Integer,db.ForeignKey('books.BookID'),nullable =False)
    ApprovedAdminID=db.Column(db.Integer,db.ForeignKey('admin.AdminID'),nullable=False)

class Feedbacks(db.Model):
    __tablename__='feedbacks'
    FeedbackID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Feedback=db.Column(db.String(500),nullable=False)
    Stars=db.Column(db.Integer,nullable=False)

    UserID=db.Column(db.Integer,db.ForeignKey('user.UserID'),nullable =False)
    BookId=db.Column(db.Integer,db.ForeignKey('books.BookID'),nullable =False)

class Transaction(db.Model):
    __tablename__='transaction'
    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    BookID = db.Column(db.Integer, db.ForeignKey('books.BookID'), nullable=False)
    Amount = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
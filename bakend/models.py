from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column ,Integer ,Text ,DateTime,Boolean 
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_bcrypt import Bcrypt


db=SQLAlchemy()
ma=Marshmallow()
bcrypt=Bcrypt()

class User(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)
    email=Column(Text,nullable=False,unique=True)
    password=Column(Text,nullable=False)
    name=Column(Text,nullable=False)
    is_librarian=Column(Boolean,nullable=False,default=False)
    latest_loggedin=Column(DateTime ,nullable=False)

    user_issue=relationship('Issues',back_populates='userIssue', cascade= "all, delete-orphan")

    user_request=relationship('Request',back_populates='userRequest', cascade= "all, delete-orphan")

    user_feedback=relationship('Feedback',back_populates='userFeedback', cascade= "all, delete-orphan")


    def __init__(self , email , password , name , latest_loggedin , is_librarian=False):
        self.email=email
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')
        self.name=name
        self.is_librarian=is_librarian
        self.latest_loggedin=latest_loggedin



class UserSchema(ma.Schema):
    class meta:
        fields=('id','email','password','name','is_librarian','latest_loggedin') 

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Section(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Text, nullable=False,unique=True)
    books=relationship('Book',back_populates='section', cascade= "all, delete-orphan")


    def __init__(self,name):
         self.name = name




class Book(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Text, nullable=False,unique=True)
    author_name=Column(Text, nullable=False)
    content=Column(Text, nullable=False)
    section_id=Column(Integer, db.ForeignKey('section.id'), nullable=False)
    section = relationship('Section', back_populates='books')

    book_issue=relationship('Issues',back_populates='bookIssue', cascade= "all, delete-orphan")

    book_request=relationship('Request',back_populates='bookRequest', cascade= "all, delete-orphan")

    book_feedback=relationship('Feedback',back_populates='bookFeedback', cascade= "all, delete-orphan")



    def __init__(self,name,author_name,content,section_id):
        self.name=name
        self.author_name=author_name
        self.content=content
        self.section_id=section_id


class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author_name', 'content', 'section_id')

book_schema = BookSchema()
books_schema = BookSchema(many=True)


class Issues(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)

    user_id=Column(Integer, db.ForeignKey('user.id'), nullable=False)
    userIssue = relationship('User', back_populates='user_issue')
    date=Column(DateTime, nullable=False)

    book_id=Column(Integer, db.ForeignKey('book.id'), nullable=False)
    bookIssue = relationship('Book', back_populates='book_issue')

class Request(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)

    user_id=Column(Integer, db.ForeignKey('user.id'), nullable=False)
    userRequest = relationship('User', back_populates='user_request')

    book_id=Column(Integer, db.ForeignKey('book.id'), nullable=False)
    bookRequest = relationship('Book', back_populates='book_request')



class Feedback(db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer, db.ForeignKey('user.id'), nullable=False)
    userFeedback = relationship('User', back_populates='user_feedback')

    book_id=Column(Integer, db.ForeignKey('book.id'), nullable=False)
    bookFeedback = relationship('Book', back_populates='book_feedback')

    
    content=Column(Text, nullable=False)




  
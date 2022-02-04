from scrapbook import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # user_scrap_set

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    # book_scrap_set

class Scrap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    page = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(120), unique=True, nullable=False)    # AWS S3에서 파일을 저장하면 주소값을 받아올 것이고, 이를 저장
    user = db.relationship('User', backref=db.backref('user_scrap_set'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book = db.relationship('Book', backref=db.backref('book_scrap_set'))
    bookId = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
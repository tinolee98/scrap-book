from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, DateTime, column
from sqlalchemy.orm import relationship, backref

from .database import Base
from datetime import datetime

scrapbook_users = Table(
    'scrapbook_users',Base.metadata,
    Column('userId', Integer, ForeignKey('user.id', ondelete="CASCADE")),
    Column('scrapbookId', Integer, ForeignKey('scrapbook.id', ondelete="CASCADE")),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    refreshToken = Column(String(120))
    # scrapbooks
    # scraps

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(120), nullable=False)
    authors = Column(String(120), nullable=False)
    publisher = Column(String(120), nullable=False)
    contents = Column(Text, nullable=False)
    thumbnail = Column(String(180), nullable=False)
    url = Column(String(180), nullable=False)

class Scrapbook(Base):
    __tablename__ = "scrapbook"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(String(20), unique=True, nullable=False)
    users = relationship('User', secondary=scrapbook_users, backref=backref('scrapbooks'))
    bookId = Column(Integer, ForeignKey('book.id'), nullable=False)
    book = relationship('Book', backref=backref('scrapbooks'))
    createdAt = Column(DateTime, default=datetime.now(), nullable=False)
    updatedAt = Column(DateTime)
    # scraps

class Scrap(Base):
    __tablename__ = "scrap"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    text = Column(Text)
    page = Column(Integer, nullable=False)
    picture = Column(String(120), nullable=False, unique=True)
    userId = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = relationship('User', backref=backref('scraps'))
    scrapbookId = Column(Integer, ForeignKey('scrapbook.id', ondelete="CASCADE"), nullable=False)
    scrapbook = relationship('Scrapbook', backref=backref('scraps'))
    createdAt = Column(DateTime, default=datetime.now(), nullable=False)
    updatedAt = Column(DateTime)

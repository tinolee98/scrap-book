from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text, DateTime, UniqueConstraint, column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

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
    uuid = Column(String(40), unique=True, nullable=False)
    users = relationship('User', secondary=scrapbook_users, backref=backref('scrapbooks', lazy='dynamic'))
    bookId = Column(Integer, ForeignKey('book.id'), nullable=False)
    book = relationship('Book', lazy='select', backref=backref('scrapbooks', lazy='select'))
    createdAt = Column(DateTime(timezone=True), default=func.now())
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    # scraps

class Scrap(Base):
    __tablename__ = "scrap"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    text = Column(Text)
    page = Column(Integer, nullable=False)
    picture = Column(String(120), nullable=False, unique=True)
    userId = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = relationship('User', backref=backref('scraps', lazy='dynamic'))
    scrapbookId = Column(Integer, ForeignKey('scrapbook.id', ondelete="CASCADE"), nullable=False)
    scrapbook = relationship('Scrapbook', backref=backref('scraps', lazy='dynamic'))
    createdAt = Column(DateTime(timezone=True), default=func.now())
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class ScrapbookStar(Base):
    __tablename__ = "scrapbook_star"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    userId = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    scrapbookId = Column(Integer, ForeignKey('scrapbook.id', ondelete='CASCADE'), nullable=False)
    is_starred = Column(Boolean, default=False, nullable=False)
    __table_args__ = (UniqueConstraint('userId', 'scrapbookId', name='_user_scrapbook_uc'),)

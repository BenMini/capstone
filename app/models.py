from flask import json
from datetime import datetime
from app import db


class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer(10))
    description = db.Column(db.String(140))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<Business {self.body}>'

    def short(self):
        print(json.loads(self.name))
        return {
            'id': self.id,
            'name': self.name
        }

    def long(self):
        print(json.loads(self.name))
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'description': self.description,
            'posts': Post.query.filter_by(Post.id == self.id).all()
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.body}>'

    def short(self):
        return {
            'id': self.id,
            'body': self.body[0:100]
        }

    def long(self):
        return {
            'id': self.id,
            'body': self.body,
            'business_id': self.business_id,
            'timestamp': self.moment(self.timestamp).fromNow()
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

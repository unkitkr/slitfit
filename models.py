from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_login import  UserMixin
import uuid
import datetime

db = SQLAlchemy()

class Users(db.Model,UserMixin):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique = True)
    date_of_joining = db.Column(db.DateTime, default = datetime.datetime.utcnow, nullable = False)
    user_links = db.relationship('UserSettings', backref="Users")

    def get_id(self):
        return self.uid
    
class UserLinks(db.Model,UserMixin):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    original_link = db.Column(db.String, nullable=False)
    short_key = db.Column(db.String(8), nullable=False)
    created_on = db.Column(db.DateTime, default = datetime.datetime.utcnow, nullable = False)
    is_active = db.Column(db.Boolean, default = True, nullable = False)
    user_backref = db.relationship("Users", backref="UserLinks")
    

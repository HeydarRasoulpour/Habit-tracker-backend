import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .users_challenge_xref import user_challenge_xref

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False, unique=True)
    last_name = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String())
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False, default='user')
    is_active = db.Column(db.Boolean(), default=True)

    auth = db.relationship("AuthTokens",back_populates="user")
    profile = db.relationship("Profiles", foreign_keys='[Profiles.user_id]', back_populates='user', cascade="all")
    challenges = db.relationship("HabitChallenges", secondary=user_challenge_xref, back_populates='users')
    habits = db.relationship("Habits", foreign_keys='[Habits.user_id]', back_populates='user', cascade="all")
    habitReminders = db.relationship("HabitReminders", foreign_keys='[HabitReminders.user_id]', back_populates='user', cascade="all")
    

    def __init__(self,first_name, last_name, username, email, phone, password, role='user', is_active=True):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.email=email
        self.phone=phone
        self.password=password
        self.role=role
        self.is_active=is_active

    def new_user_obj():
        return Users('','','','','','','user',True)  


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id','first_name','last_name','username', 'email', 'phone', 'role', 'is_active', 'challenges']   

    user_id=ma.fields.UUID()
    first_name=ma.fields.String(required=True)
    last_name=ma.fields.String(required=True)
    username=ma.fields.String(required=True)
    email=ma.fields.String(required=True)  
    phone=ma.fields.String()   
    role=ma.fields.String(required=True, dump_default='user')
    is_active=ma.fields.Boolean(allow_none=True, dump_default=True)

    challenges = ma.fields.Nested("HabitChallengesSchema", many=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
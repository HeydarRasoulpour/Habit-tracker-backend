import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from datetime import datetime

from db import db
from .habit_category_xref import habit_category_xref

class Habits(db.Model):
    __tablename__="Habits"

    habit_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    title = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    color = db.Column(db.String())
    frequency_per_week = db.Column(db.Integer())
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.String())
    is_active = db.Column(db.Boolean(), default=True)
    image_url = db.Column(db.String)


    user = db.relationship("Users", foreign_keys='[Habits.user_id]', back_populates = 'habits')
    habitReminder = db.relationship("HabitReminders", foreign_keys='[HabitReminders.habit_id]',back_populates = 'habit', cascade="all")
    categories = db.relationship("HabitCategories", secondary=habit_category_xref, back_populates='habits')
    habit_tracking = db.relationship("HabitTracking", foreign_keys='[HabitTracking.habit_id]',back_populates = 'habit', cascade="all")



    # def __init__(self,user_id,title,description, color, frequency_per_week,image_url, start_date,end_date,is_active=True):
    #     self.user_id=user_id
    #     self.title=title
    #     self.description=description
    #     self.color=color
    #     self.frequency_per_week=frequency_per_week
    #     self.start_date=start_date
    #     self.end_date=end_date
    #     self.is_active=is_active
    #     self.image_url = image_url

    # def new_habit_obj():
        # return Habits('','','',0,'','',datetime.now(),True)
    # def new_habit_obj():
        # return Habits()

class HabitsSchema(ma.Schema):
    class Meta:
        fields = ['habit_id', 'title', 'description', 'color', 'frequency_per_week','image_url', 'start_date', 'end_date', 'is_active', 'user','categories']

    habit_id= ma.fields.UUID()
    title=ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    color = ma.fields.String(allow_none = True)
    frequency_per_week = ma.fields.Integer()
    start_date=ma.fields.DateTime(required=True)
    end_date=ma.fields.String(allow_none=True)
    is_active=ma.fields.Boolean(allow_none=True, dump_default=True)
    image_url = ma.fields.String(allow_none=True)

    user = ma.fields.Nested("UsersSchema")
    categories = ma.fields.Nested("HabitCategoriesSchema", many=True, exclude=['habits'])

habit_schema=HabitsSchema()
habits_schema=HabitsSchema(many=True)




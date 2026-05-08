# import uuid
# from sqlachamy.dialects.postgresql import UUID
# import marshmellow as ma
# from datetime import datetime

# from db import db

# class Files(db.Modal):
#     __tablename__ = 'Files'

#     file_id = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
#     file_name = db.Column(db.string(), nullable = False)
#     habit_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Habit.habit_id"))
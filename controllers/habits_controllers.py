from flask import request, jsonify

from db import db
from models.habits import Habits, habit_schema, habits_schema
from models.habit_categories import HabitCategories
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth, authenticate
from models.habit_category_xref import habit_category_xref
from services.media_service import upload_habit_image


# @authenticate_return_auth
# def add_habit(auth_info):
#     post_data = request.form if request.form else request.json
#     file = request.files.get("image")

#     new_habit = Habits.new_habit_obj()
#     populate_obj(new_habit, post_data)

#     new_habit.user_id = auth_info.user_id

#     if file:
#         image_url = upload_habit_image(file)
#         new_habit.image_url = image_url

#     try:
#         db.session.add(new_habit)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print("ERROR",str(e))
#         return jsonify({"message":str(e)}), 400
    
#     return jsonify({"message":"habit added","result": habit_schema.dump(new_habit)}), 201

@authenticate_return_auth
def add_habit(auth_info):
    post_data = request.form
    file = request.files.get("image")

    new_habit = Habits()

    from datetime import datetime

    new_habit.title = post_data.get("title")
    new_habit.description = post_data.get("description")
    new_habit.color = post_data.get("color")

    if post_data.get("frequency_per_week"):
        new_habit.frequency_per_week = int(post_data.get("frequency_per_week"))

    if post_data.get("start_date"):
        new_habit.start_date = datetime.fromisoformat(post_data.get("start_date"))

    new_habit.end_date = post_data.get("end_date")
    new_habit.is_active = post_data.get("is_active") == "true"

    new_habit.user_id = auth_info.user_id

    if file:
        image_url = upload_habit_image(file)
        new_habit.image_url = image_url

    try:
        db.session.add(new_habit)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        return jsonify({"message": str(e)}), 400

    return jsonify({
        "message": "habit added",
        "result": habit_schema.dump(new_habit)
    }), 201



@authenticate_return_auth
def get_all_habits(auth_info):
    
    user_id = auth_info.user_id
    habit_query = db.session.query(Habits).filter(Habits.user_id == user_id).all()
   
    if not habit_query:
        return jsonify({"message": "habits not founded."}),400

    return jsonify({"message":"habits found", "results":habits_schema.dump(habit_query)}),200

    



@authenticate_return_auth
def get_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id
    if not habit_query:
        return jsonify({"message":"habit not found"}), 404
    
    if auth_info.user_id == user_id:
        return jsonify({"message":"habit found", "result": habit_schema.dump(habit_query)}), 200

    return  jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def get_habits_by_category(category_id, auth_info):
    habit_query = db.session.query(Habits).join(habit_category_xref).filter(habit_category_xref.c.category_id == category_id).all()
    user_id = habit_query[0].user.user_id
    if not habit_query:
        return jsonify({"message":"habit not found"}), 404
    
    if auth_info.user_id == user_id:
        return jsonify({"message":"habit found", "result":habits_schema.dump(habit_query)}), 200

    return  jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def add_habit_to_category(auth_info):
    post_data = request.form if request.form else request.json
    
    habit_id = post_data.get("habit_id")
    category_id = post_data.get("category_id")

    habit_query = db.session.query(Habits).filter(Habits.habit_id==habit_id).first()
    category_query = db.session.query(HabitCategories).filter(HabitCategories.category_id==category_id).first()

    
    if auth_info.user_id == user_id or auth_info.role == 'admin':

        if not habit_query:
            return jsonify({"message": "habit not found"}), 404

        if not category_query:
            return jsonify({"message":"category not found"}),404
    
        if category_query in habit_query.categories:
            return jsonify({"message": "habits already in this category"}), 400
    
        user_id = habit_query.user_id
        habit_query.categories.append(category_query)

        db.session.commit()
        return jsonify({"message":"habit added to category", "result": habit_schema.dump(habit_query)}),200
    
    return jsonify({"message":"unathorized"}),403



@authenticate_return_auth
def update_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    post_data = request.form if request.form else request.json
    user_id = habit_query.user_id

    if not habit_query:
        return jsonify({"message":"habit not found"}), 404

    if auth_info.user_id == user_id:
        populate_obj(habit_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "habit updated", "result": habit_schema.dump(habit_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id
    if auth_info.user_id == user_id:
        if not habit_query:
            return jsonify({"message": "no habit with provided id founded."}),404
    
        db.session.delete(habit_query)
        db.session.commit()

        return jsonify({"message":"habit deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    




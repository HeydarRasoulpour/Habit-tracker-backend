from flask import Blueprint

import controllers

habit_blueprint = Blueprint('habit_blueprint', __name__)

@habit_blueprint.route('/habit', methods=['POST'])
def add_habit_route():
    return controllers.add_habit()


@habit_blueprint.route('/habits', methods=['GET'])
def get_all_habits_route():
    return controllers.get_all_habits()

@habit_blueprint.route('/category/habit/', methods=['POST'])
def add_habit_to_category_route():
    return controllers.add_habit_to_category()


@habit_blueprint.route('/habit/<habit_id>', methods=['GET'])
def get_habit_by_id_route(habit_id):
    return controllers.get_habit_by_id(habit_id)

@habit_blueprint.route("/habits/<uuid:category_id>", methods = ['GET'])
def get_habits_by_category_route(category_id):
    return controllers.get_habits_by_category(category_id)


@habit_blueprint.route('/habit/<habit_id>', methods=['PUT'])
def update_habit_by_id_route(habit_id):
    return controllers.update_habit_by_id(habit_id)


@habit_blueprint.route('/habit/delete/<habit_id>', methods=['DELETE'])
def delete_habit_by_id_route(habit_id):
    return controllers.delete_habit_by_id(habit_id)
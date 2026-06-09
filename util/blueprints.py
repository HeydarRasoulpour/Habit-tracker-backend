import routes

def register_blueprint(app):
    app.register_blueprint(routes.auth_token_blueprint)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.profile_blueprint)
    app.register_blueprint(routes.habit_blueprint)
    app.register_blueprint(routes.reminders_blueprint)
    app.register_blueprint(routes.challenges_blueprint)
    app.register_blueprint(routes.tracking_blueprint)
    app.register_blueprint(routes.category)

from cloudinary.uploader import upload

def upload_habit_image(file):
    """
    file: werkzeug.FileStorage from Flask request.files
    returns: URL of uploaded image
    """
    result = upload(file, folder="habit-tracker")  # optional folder
    return result.get("secure_url")  # this is the URL you save in DB
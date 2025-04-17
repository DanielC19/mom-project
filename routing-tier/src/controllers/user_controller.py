from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User  # Asegúrate de que la ruta sea correcta

class UserController:
    def __init__(self, db):
        self.db = db

    def create_user(self, username, password):
        if not username or not password:
            return {"success": False, "message": "Missing username or password"}
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"success": False, "message": "Username alredy registrated."}
        
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            self.db.session.add(new_user)
            self.db.session.commit()
            return {"success": True, "message": "User created successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error creating user: {str(e)}"}

    def login_user(self, username, password):
        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and check_password_hash(existing_user.password, password):
                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Invalid username or password"}
        except Exception as e:
            return {"success": False, "message": f"Error logging in: {str(e)}"}
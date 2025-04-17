from flask import Blueprint, request, jsonify
from src.controllers.user_controller import UserController
from src.utils.response_utils import generate_response, log_error  
from flask_jwt_extended import create_access_token  
from src.utils.database import db  

user_bp = Blueprint('user', __name__)
user_controller = UserController(db)  

@user_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not data["password"] or not data["username"]:
            return jsonify({'error': 'Username and password required.'}), 400
        response = user_controller.create_user(data["username"], data["password"])
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error creating user: {str(e)}")
        return generate_response(False, "Failed to create user")

@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        if not data["password"] or not data["username"]:
            return jsonify({'error': 'Username and password required.'}), 400
        response = user_controller.login_user(data["username"], data["password"])
        if response["success"]:
            token = create_access_token(identity=data["username"])
            return jsonify({"success": True, "message": response["message"], "token": token})
        else:
            return generate_response(False, response["message"])
    except Exception as e:
        log_error(f"Error logging in user: {str(e)}")
        return generate_response(False, "Failed to log in user")
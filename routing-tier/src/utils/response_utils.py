def generate_response(success, message, data=None):
    from flask import jsonify

    response = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data

    return jsonify(response)

def log_error(error_message):
    import logging

    logging.error(error_message)

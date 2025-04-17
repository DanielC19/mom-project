def validate_input(data, schema):
    from jsonschema import validate, ValidationError

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        raise e

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
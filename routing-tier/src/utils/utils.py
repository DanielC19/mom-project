def validate_input(data, schema):
    from jsonschema import validate, ValidationError

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        raise e
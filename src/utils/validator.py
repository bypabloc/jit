from datetime import datetime
from re import match as re_match
from uuid import UUID


class Validator:
    _schema: dict = None
    _errors: dict = None

    def __init__(self, schema):
        self._schema = schema
        self._errors = {}

    def validate(self, data):
        root_type = self._schema.get("type", "object")
        self._validate_value(data, self._schema, "", root_type)

    def is_valid(self):
        return len(self._errors) == 0

    def get_errors(self):
        return self._errors

    def _add_error(self, path, error_message):
        keys = path.split(".")
        current = self._errors
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        if keys[-1] not in current:
            current[keys[-1]] = []
        current[keys[-1]].append(error_message)

    def _validate_value(self, value, schema, path, root_type=None):
        data_types = schema.get("type", root_type)

        if not isinstance(data_types, list):
            data_types = [data_types]

        validators = {
            "string": self._validate_string,
            "number": self._validate_number,
            "array": self._validate_array,
            "object": self._validate_object,
            "boolean": self._validate_boolean,
        }

        valid = False
        error_messages = []
        for data_type in data_types:
            validator = validators.get(data_type)
            if not validator:
                error_messages.append(f"Unknown data type '{data_types}'")
            else:
                valid = validator(value, schema, path, check_only=True)

            if valid:
                break

        if not valid:
            for error_message in error_messages:
                self._add_error(path, error_message)

    def _validate_object(self, obj, schema, path="", check_only=False):
        if schema["type"] == "object":
            for key, prop_schema in schema["properties"].items():
                if key in obj:
                    self._validate_value(obj[key], prop_schema, f"{path}.{key}" if path else key)
                elif "default" in prop_schema:
                    obj[key] = prop_schema["default"]
                elif "required" in schema and key in schema["required"]:
                    self._add_error(f"{path}.{key}", "Required property is missing")

    def _validate_boolean(self, value, schema, path, check_only=False):
        if not isinstance(value, bool):
            if not check_only:
                self._add_error(path, "should be a boolean")
            return False
        return True

    def _validate_string(self, value, schema, path, check_only=False):
        if not isinstance(value, str):
            if not check_only:
                self._add_error(path, f"should be of type 'string', but got '{type(value).__name__}'")
            return False

        if "minLength" in schema and len(value) < schema["minLength"]:
            self._add_error(path, f"should have a minimum length of {schema['minLength']}")

        if "maxLength" in schema and len(value) > schema["maxLength"]:
            self._add_error(path, f"should have a maximum length of {schema['maxLength']}")

        if "format" in schema:
            format_validators = {
                "email": self._validate_string_email,
                "uri": self._validate_string_uri,
                "date": self._validate_string_date,
                "datetime": self._validate_string_datetime,
                "time": self._validate_string_time,
                "uuid-v4": self._validate_string_uuid_v4,
                "duration": self._validate_string_duration,
            }
            format_validator = format_validators.get(schema["format"])
            if not format_validator:
                self._add_error(path, f"Unknown format '{schema['format']}'")
            elif format_validator and not format_validator(value):
                self._add_error(path, f"should match the format '{schema['format']}'")

        if "pattern" in schema:
            pattern = schema["pattern"]
            if not self._validate_pattern(pattern, value):
                self._add_error(path, f"Value '{value}' does not match pattern '{pattern}'")
        return True

    def _validate_number(self, value, schema, path, check_only=False):
        if not isinstance(value, (int, float)):
            if not check_only:
                self._add_error(path, f"should be of type 'number', but got '{type(value).__name__}'")
            return False

        if "minimum" in schema and value < schema["minimum"]:
            self._add_error(path, f"should be greater than or equal to {schema['minimum']}")

        if "maximum" in schema and value > schema["maximum"]:
            self._add_error(path, f"should be less than or equal to {schema['maximum']}")
        return True

    def _validate_array(self, value, schema, path, check_only=False):
        if not isinstance(value, list):
            if not check_only:
                self._add_error(path, f"should be of type 'array', but got '{type(value).__name__}'")
            return False

        if "minItems" in schema and len(value) < schema["minItems"]:
            self._add_error(path, f"should have at least {schema['minItems']} items")

        if "uniqueItems" in schema and schema["uniqueItems"] and len(value) != len(set(value)):
            self._add_error(path, "should have unique items")

        if "items" in schema:
            for idx, item in enumerate(value):
                self._validate_value(item, schema["items"], f"{path}[{idx}]")
        return True

    def _validate_string_email(self, value):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re_match(email_regex, value) is not None

    def _validate_string_uri(self, value):
        uri_regex = r"(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        return re_match(uri_regex, value) is not None

    def _validate_string_date(self, value):
        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    def _validate_string_datetime(self, value):
        date_time_format = "%Y-%m-%dT%H:%M:%SZ"
        try:
            datetime.strptime(value, date_time_format)
            return True
        except ValueError:
            return False

    def _validate_string_time(self, value):
        time_format = "%H:%M:%S"
        try:
            datetime.strptime(value, time_format)
            return True
        except ValueError:
            return False

    def _validate_string_duration(self, value):
        duration_regex = r"^P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d{1,9})?)S)?)?$"
        return re_match(duration_regex, value) is not None

    def _validate_string_uuid_v4(self, value):
        uuid_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        return re_match(uuid_regex, value) is not None

    def _validate_pattern(self, pattern, value):
        return re_match(pattern, value) is not None


if __name__ == "__main__":
    # Definición de la clase Validator (con todos los cambios anteriores)
    schema = {
        "title": "Employee",
        "description": "An employee in the company",
        "type": "object",
        "properties": {
            "name": {
            "description": "Name of the employee",
            "type": "string",
            "minLength": 3,
            "maxLength": 20
            },
            "email": {
            "description": "Email address of the employee",
            "type": "string",
            "format": "email"
            },
            "birthDate": {
            "description": "Birth date of the employee",
            "type": "string",
            "format": "date"
            },
            "birthDateTime": {
            "description": "Birth date and time of the employee",
            "type": "string",
            "format": "datetime",
            "default": "2016-01-01T00:00:00Z"
            },
            "birthTime": {
            "description": "Birth time of the employee",
            "type": "string",
            "format": "time"
            },
            "duration": {
            "description": "Duration of the employee's contract",
            "type": "string",
            "format": "duration"
            },
            "age": {
            "description": "Age of the employee",
            "type": "number",
            "minimum": 18,
            "maximum": 60
            },
            "salary": {
            "description": "Salary of the employee",
            "type": ["number", "string"],
            "minimum": 1000,
            "maximum": 10000
            },
            "contactNo": {
            "description": "Contact numbers of the employee",
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
            },
            "minItems": 1,
            "uniqueItems": True
            },
            "address": {
            "description": "Address of the employee",
            "type": "object",
            "properties": {
                "postalCode": {
                "type": "string",
                "pattern": "^[0-9]{5}$"
                },
                "street": {
                "type": "string",
                "minLength": 18,
                "maxLength": 60
                },
                "city": {
                "type": "string"
                },
                "country": {
                "type": "string",
                "default": "Malaysia"
                },
                "isPrimary": {
                "type": "boolean",
                "default": True
                }
            },
            "required": ["postalCode", "street", "city"]
            },
            "projects": {
            "description": "Projects the employee has worked on",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "name": {
                    "type": "string"
                },
                "duration": {
                    "type": "string",
                    "format": "duration"
                }
                },
                "required": ["name", "duration"]
            }
            }
        },
        "required": ["name", "email", "age", "address"]
        }


    # Ejemplo de un objeto válido
    valid_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "birthDate": "1990-05-01",
        "birthDateTime": "1990-05-01T08:30:00Z",
        "birthTime": "08:30:00",
        "duration": "P1Y2M10DT2H30M",
        "age": 33,
        "salary": 5000,
        "contactNo": [
            "+1 234-567-8910"
        ],
        "address": {
            "postalCode": "12345",
            "street": "123 Main Street Apt 4 Las Altas",
            "city": "New York",
            "country": "USA",
            "isPrimary": True
        },
        "projects": [
            {
            "name": "Project A",
            "duration": "P2Y6M"
            },
            {
            "name": "Project B",
            "duration": "P1Y3M15D"
            }
        ]
        }


    # Ejemplo de un objeto inválido
    invalid_data = {
        "name": "JD",
        "email": "john.doe@example",
        "birthDate": "1990/05/01",
        "birthDateTime": "1990-05-01 08:30:00",
        "birthTime": "083000",
        "duration": "1Y2M10DT2H30M",
        "age": 17,
        "salary": 90000,
        "contactNo": [
            "+1 234-567-8910",
            "+1 234-567-8910"
        ],
        "address": {
            "postalCode": "1234A",
            "street": "123",
            "city": "New York"
        },
        "projects": [
            {
            "name": "Project A",
            "duration": "2Y6M"
            },
            {
            "name": "Project B",
            "duration": "1Y3M15D"
            }
        ]
        }

    validator = Validator(schema)

    # Validando el objeto válido
    validator.validate(valid_data)
    print("Valid object errors:", validator.get_errors())  # Debería estar vacío []

    # Validando el objeto inválido
    validator.validate(invalid_data)
    print("Invalid object errors:", validator.get_errors())  # Debería mostrar el error de patrón

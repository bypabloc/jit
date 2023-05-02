from re import compile as re_compile
from re import error as re_error
from re import escape as re_escape
from re import match as re_match


class Validator:
    _schema: dict = None
    _errors: dict = None

    DATETIME_FORMATS = {
        'DATE': {
            '%b': r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",  # Abreviatura del mes (3 caracteres)
            '%d': r"(0[1-9]|[12][0-9]|3[01])",                           # Día del mes (01-31)
            '%Y': r"\d{4}",                                              # Año en formato de 4 dígitos
            '%a': r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)",                      # Abreviatura del día de la semana (3 caracteres)
            '%A': r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",  # Nombre completo del día de la semana
            '%B': r"(January|February|March|April|May|June|July|August|September|October|November|December)",  # Nombre completo del mes
            '%w': r"[0-6]",                                              # Día de la semana como número (0-6, domingo=0)
            '%m': r"(0[1-9]|1[012])",                                    # Mes como número (01-12)
            '%y': r"\d{2}",                                              # Año en formato de 2 dígitos (sin siglo)
            '%j': r"(00[1-9]|0[1-9]\d|[12]\d{2}|3[0-5]\d|366)",          # Número del día en el año (001-366)
            '%W': r"(0[0-9]|[1-4][0-9]|5[0-3])",                         # Número de la semana del año (00-53, lunes=primer día)
            '%U': r"(0[0-9]|[1-4][0-9]|5[0-3])",                         # Número de la semana del año (00-53, domingo=primer día)
        },
        'TIME': {
            '%H': r"([01]\d|2[0-3])",                                    # Hora (00-23)
            '%M': r"([0-5]\d)",                                          # Minuto (00-59)
            '%S': r"([0-5]\d)",                                          # Segundo (00-59)
            '%p': r"(AM|PM)",                                            # AM/PM para la hora
            '%f': r"\d{6}",                                              # Micro segundo (000000-999999)
            '%Z': r"[A-Z]{3}",                                           # Zona horaria (ejemplo: CST)
            '%z': r"[+-]\d{4}",                                          # Desplazamiento UTC (ejemplo: +0600)
        },
    }

    def __init__(self, schema):
        self._schema = schema
        self._errors = {}

    def validate(self, data):
        root_type = self._schema.get("type", "object")
        self.__validate_value(data, self._schema, "", root_type)

    def is_valid(self):
        return bool(self.errors)

    def get_errors(self):
        return self._errors

    def __add_error(self, path, error_message):
        keys = path.split(".")
        current = self._errors
        for key in keys[:-1]:
            if key.endswith(']'):
                index = int(key[key.index('[') + 1:key.index(']')])
                key = key[:key.index('[')]
                if key not in current:
                    current[key] = []
                while len(current[key]) <= index:
                    current[key].append({})
                current = current[key][index]
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]

        last_key = keys[-1]
        if last_key.endswith(']'):
            index = int(last_key[last_key.index('[') + 1:last_key.index(']')])
            last_key = last_key[:last_key.index('[')]
            if last_key not in current:
                current[last_key] = []
            while len(current[last_key]) <= index:
                current[last_key].append(None)  # Change here: Use None instead of []
            current[last_key][index] = error_message  # Change here: Assign the error_message directly
        else:
            if last_key not in current:
                current[last_key] = []
            current[last_key].append(error_message)

    def __validate_value(self, value, schema, path, root_type=None):
        data_type = schema.get("type", root_type)
        if not isinstance(data_type, str):
            self.__add_error(path, f"Should be of type 'string', but got '{type(data_type).__name__}'")
            return False

        validators = {
            "string": self.__validate_string,
            "number": self.__validate_number,
            "integer": self.__validate_integer,
            "array": self.__validate_array,
            "object": self.__validate_object,
            "boolean": self.__validate_boolean,
        }

        validator = validators.get(data_type)
        if not validator:
            self.__add_error(path, f"Unknown data type '{data_type}'")
            return False
        is_valid = validator(value, schema, path)
        if not is_valid:
            return False
        return value

    def __validate_object(self, obj, schema, path=""):
        if not isinstance(obj, dict):
            self.__add_error(path, f"should be of type 'object', but got '{type(obj).__name__}'")
            return False

        properties = schema.get("properties", {})
        propertyNames = schema.get("propertyNames", {})
        if propertyNames:
            pattern = propertyNames.get('pattern')
            if pattern:
                regex = re_compile(pattern)
                for key in properties.keys():
                    if not regex.match(key):
                        key = f"'{key}'" if key else "''"
                        self.__add_error(key, f"Invalid property name: should match pattern {pattern}")
                        return False

        is_valid = True
        additional_properties = schema.get("additionalProperties", True)
        for key, prop_schema in properties.items():
            value = obj.get(key)
            required = prop_schema.get("required")
            default = prop_schema.get("default")
            if required and value is None:
                self.__add_error(key, "Required property is missing")
                continue
            if key in obj:
                if default and value is None:
                    obj[key] = default
                    value = default
                if value is None:
                    self.__add_error(key, "Required property is missing")
                    continue
                validated = self.__validate_value(obj[key], prop_schema, f"{path}.{key}" if path else key)
                if not validated and is_valid:
                    is_valid = False

        if not additional_properties:
            extra_keys = set(obj.keys()) - set(properties.keys())
            if extra_keys:
                for key in extra_keys:
                    self.__add_error(path, f"Additional property '{key}' not allowed")
                is_valid = False

        return is_valid

    def __validate_boolean(self, value, schema, path):
        if not isinstance(value, bool):
            self.__add_error(path, "should be a boolean")
            return False
        return True

    def __validate_string(self, value, schema, path):
        if not isinstance(value, str):
            self.__add_error(path, f"should be of type 'string', but got '{type(value).__name__}'")
            return False

        if "minLength" in schema and len(value) < schema["minLength"]:
            self.__add_error(path, f"should have a minimum length of {schema['minLength']}")
            return False

        if "maxLength" in schema and len(value) > schema["maxLength"]:
            self.__add_error(path, f"should have a maximum length of {schema['maxLength']}")
            return False

        if "format" in schema:
            format_validators = {
                "email": self.__validate_string_email,
                "uri": self.__validate_string_uri,
                "date": self.__validate_string_date,
                "datetime": self.__validate_string_datetime,
                "time": self.__validate_string_time,
                "uuid-v4": self.__validate_string_uuid_v4,
                "duration": self.__validate_string_duration,
            }
            format_validator = format_validators.get(schema["format"])
            if not format_validator:
                self.__add_error(path, f"Unknown format '{schema['format']}'")
            validated, error_message = format_validator(value=value)
            if not validated:
                self.__add_error(path, error_message)
                return False

        if "pattern" in schema:
            pattern = schema["pattern"]
            if not self.__is_valid_regex(pattern):
                self.__add_error(path, f"Invalid regular expression '{pattern}'")
                return False
            if not self.__validate_pattern(pattern, value):
                self.__add_error(path, f"Value '{value}' does not match pattern '{pattern}'")
                return False
        return True

    def __validate_string_email(self, value):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        is_valid = re_match(email_regex, value)
        if not is_valid:
            return False, "should be a valid email address"
        return True, ""

    def __validate_string_uri(self, value):
        uri_regex = r"(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\((?:[^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\((?:[^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’$]))"
        is_valid = re_match(uri_regex, value)
        if not is_valid:
            return False, "should be a valid URI"
        return True, ""

    def __validate_string_date(self, value):
        date_format_mapping = self.DATETIME_FORMATS.get('DATE', {})
        format_mapping = {**date_format_mapping}
        regex = "^" + "".join([format_mapping.get(char, re_escape(char)) for char in value]) + "$"
        is_valid = re_match(regex, value)
        if not is_valid:
            return False, "Should be a valid date"
        return True, ""

    def __validate_string_datetime(self, value):
        date_format_mapping = self.DATETIME_FORMATS.get('DATE', {})
        time_format_mapping = self.DATETIME_FORMATS.get('TIME', {})
        format_mapping = {**date_format_mapping, **time_format_mapping}
        regex = "^" + "".join([format_mapping.get(char, re_escape(char)) for char in value]) + "$"
        is_valid = re_match(regex, value)
        if not is_valid:
            return False, "Should be a valid datetime"
        return True, ""

    def __validate_string_time(self, value):
        time_format_mapping = self.DATETIME_FORMATS.get('TIME', {})
        format_mapping = {**time_format_mapping}
        regex = "^" + "".join([format_mapping.get(char, re_escape(char)) for char in value]) + "$"
        is_valid = re_match(regex, value)
        if not is_valid:
            return False, "Should be a valid time"
        return True, ""

    def __validate_string_duration(self, value):
        duration_regex = r"^P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d{1,9})?)S)?)?$"
        is_valid = re_match(duration_regex, value)
        if not is_valid:
            return False, "should be a valid duration"
        return True, ""

    def __validate_string_uuid_v4(self, value):
        uuid_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        is_valid = re_match(uuid_regex, value)
        if not is_valid:
            return False, "should be a valid UUIDv4"
        return True, ""

    def __validate_pattern(self, pattern, value):
        return re_match(pattern, value) is not None

    def __is_valid_regex(self, regex):
        try:
            re_compile(regex)
            return True
        except re_error:
            return False

    def __validate_number(self, value, schema, path):
        if not isinstance(value, (int, float)):
            self.__add_error(path, f"should be of type 'number', but got '{type(value).__name__}'")
            return False

        if "minimum" in schema and value < schema["minimum"]:
            self.__add_error(path, f"should be greater than or equal to {schema['minimum']}")

        if "maximum" in schema and value > schema["maximum"]:
            self.__add_error(path, f"should be less than or equal to {schema['maximum']}")
        return True

    def __validate_integer(self, value, schema, path):
        if not isinstance(value, (int, str, float)):
            self.__add_error(path, f"should be of type 'integer', but got '{type(value).__name__}'")
            return False

        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                self.__add_error(path, f"should be of type 'integer', but got '{type(value).__name__}'")
                return False

        if isinstance(value, float):
            if not value.is_integer():
                self.__add_error(path, "should be an integer")
                return False
            value = int(value)

        if "multipleOf" in schema and value % schema["multipleOf"] != 0:
            self.__add_error(path, f"should be a multiple of {schema['multipleOf']}")

        if "minimum" in schema and value < schema["minimum"]:
            self.__add_error(path, f"should be greater than or equal to {schema['minimum']}")

        if "maximum" in schema and value > schema["maximum"]:
            self.__add_error(path, f"should be less than or equal to {schema['maximum']}")
        return True

    def __validate_array(self, value, schema, path):
        if not isinstance(value, list):
            self.__add_error(path, f"should be of type 'array', but got '{type(value).__name__}'")
            return False

        if "minItems" in schema and len(value) < schema["minItems"]:
            self.__add_error(path, f"should have at least {schema['minItems']} items")
            return False

        if "uniqueItems" in schema and schema["uniqueItems"] and len(value) != len(set(value)):
            self.__add_error(path, "should have unique items")
            return False

        allow_empty_value = schema.get('allowEmptyValue', True)
        allowed_values = schema.get('allowedValues', [])
        default_value = schema.get('default')
        not_allowed_values = schema.get('notAllowedValues', [])

        is_valid = True
        result = []
        for index, item in enumerate(value):
            item_schema = schema['items']
            validated_item = self.__validate_value(item, item_schema, path)

            if allow_empty_value or validated_item != '':
                result.append(validated_item)
                is_valid = False if is_valid else is_valid

            if allowed_values and validated_item not in allowed_values:
                self.__add_error(path, f"Value should be one of {allowed_values}")
                is_valid = False if is_valid else is_valid

            if not_allowed_values and validated_item in not_allowed_values:
                self.__add_error(path, f"Value {validated_item} is not allowed")
                is_valid = False if is_valid else is_valid

            if default_value is not None and validated_item is None:
                result[-1] = default_value

        return is_valid


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
                "maxLength": 20,
                "required": True
            },
            "age": {
                "description": "Age of the employee",
                "type": "integer",
                "minimum": 18,
                "maximum": 99
            },
            "email": {
                "description": "Email address of the employee",
                "type": "string",
                "format": "email",
                "required": True
            },
            "cellphone": {
                "description": "Cellphone number of the employee",
                "type": "string",
                "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
            },
            "birthDate": {
                "description": "Birth date of the employee",
                "type": "string",
                "format": "date",
                "default": "2016-01-01",
                "min": "1900-01-01",
                "max": "2016-01-01"
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
            "salary": {
                "description": "Salary of the employee",
                "type": "number",
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
                "allowEmptyValue": False,
                "allowedValues": ["+60123456789", "+6012-345-6789"],
                "notAllowedValues": ["+60123456781", "+6012-345-6782"],
                "default": ["+60123456789"],
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
                    },
                    "referencies": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
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
                }
            }
        },
        "additionalProperties": False,
        "propertyNames": {
            "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
        },
    }

    # Ejemplo de un objeto válido
    valid_data = {
        "&%$%(/)(/(?¡?=^`^`name": "John Doe Jr.",
        "name": "John Doe Jr.",
        "email": "john.doe@example.com",
        "age": 30,
        "cellphone": "(888)555-1212",
        "birthDate": "1990-05-01",
        "birthDateTime": "1990-05-01T08:30:00Z",
        "birthTime": "08:30:00",
        "duration": "P1Y2M10DT2H30M",
        "salary": 5000.0,
        "contactNo": [
            "+60123456789"
        ],
        "address": {
            "postalCode": "12345",
            "street": "123 Main Street Apt 4 Las Altas",
            "city": "New York",
            "country": "USA",
            "isPrimary": True,
            "referencies": [
                "Near the park",
                "Beside the church"
            ]
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
        "email": "john.doe@example",
        "age": 25.5,
        "cellphone": "(800)FLOWERS",
        "birthDate": "1990/05/01",
        "birthDateTime": "1990-05-01 08:30:00",
        "birthTime": "083000",
        "duration": "1Y2M10DT2H30M",
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

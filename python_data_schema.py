#################
# Decorators
#################

def canonicalize_args(if_dict):
    'Returns a list of validators (functions that take one argument and return a boolean)'
    def decorator(func):
        def wrapper(*args):
            if type_is_(dict)(args[0]):
                args = if_dict(args[0])
            elif type_is_(list)(args[0]):
                args = args[0]
            else:
                args = list(args)
            return func(args)
        return wrapper
    return decorator

# {key : value} are {validator generator : validator generator argument}
# key(value) returns a validator
def eval_function_argument_pairs(func_arg_pairs):
    return [k(v) for k,v in func_arg_pairs.items()]

# {key : value} are {validator for key : validator for value} (not validator generators!)
def translate_shorthand_syntax(key_value_validators):
    args = []
    for key_validator, value_validator in key_value_validators.items():
        if or_(type_is_(str), type_is_(int))(key_validator):
            key_validator = equals_(key_validator)
        args.append(and_(key_(key_validator), value_(value_validator)))
    return args


########################
# Validator generators  (Each returns a validator function)
########################

### Logical operator ###
# Each combines validators and returns a validator
@canonicalize_args(if_dict=eval_function_argument_pairs)
def and_(validators):
    def validator(data):
        for val in validators:
            if not val(data):
                return False
        return True
    return validator
### Logical operator ###
@canonicalize_args(if_dict=translate_shorthand_syntax)
def or_(validators):
    def validator(data):
        for val in validators:
            if val(data):
                return True
        return False
    return validator

def for_each_item_(element_validator):
    'for each item in data (list or dict)'
    def anonymous(list_or_dict_data):
        if type_is_(dict)(list_or_dict_data):
            list_or_dict_data = list_or_dict_data.items()
        return all(map(element_validator, list_or_dict_data))
    return anonymous

equals_ = lambda value: lambda data: data == value

is_ =     lambda value: lambda data: data is value

type_is_ = lambda value: lambda data: type(data) is value


######################
# Validator modifiers (returns a validator)
######################
def key_(validation_func):
    def wrapper(data):
        return validation_func(data[0])
    return wrapper

def value_(validation_func):
    def wrapper(data):
        return validation_func(data[1])
    return wrapper

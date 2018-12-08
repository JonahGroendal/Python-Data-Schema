__author__ = "Jonah Groendal"

#################################
# Decorators for and_() and or_()
#################################

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


###########################################################
# Validator generators  (Each returns a validator function)
###########################################################

def is_(value):
	def validator(data):
		return data is value
	return validator

def equals_(value):
	def validator(data):
		return data == value
	return validator

def greater_than_(value):
	def validator(data):
		return data > value
	return validator

def less_than_(value):
	def validator(data):
		return data < value
	return validator

@canonicalize_args(if_dict=eval_function_argument_pairs)
def and_(validators):
    'ands together validators'
    def validator(data):
        for val in validators:
            if not val(data):
                return False
        return True
    return validator

@canonicalize_args(if_dict=translate_shorthand_syntax)
def or_(validators):
    'ors together validators'
    def validator(data):
        for val in validators:
            if val(data):
                return True
        return False
    return validator

def for_each_item_(element_validator):
    'for each item in data (list or dict)'
    def validator(list_or_dict_data):
        if type_is_(dict)(list_or_dict_data):
            list_or_dict_data = list_or_dict_data.items()
        return all(map(element_validator, list_or_dict_data))
    return validator

# Predefined example of how to use data_()
def type_is_(value):
	return data_(type)(is_(value))


##########################################################################
# Validator data modifiers (modifies data before it's passed to validator)
##########################################################################

def data_(data_modifier):
	def wrapper(validation_func):
		def validator(data):
			return validation_func(data_modifier(data))
		return validator
	return wrapper

def key_(validation_func):
	return data_(atIndex(0))(validation_func)

def value_(validation_func):
	return data_(atIndex(1))(validation_func)


##########################################
# data_modifier funcs for use with data_()
##########################################

def atIndex(i):
	return lambda data: data[i]


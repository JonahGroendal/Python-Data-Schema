### Python Data Schema
is a library for defining and validating recursive data structures in Python using functional programming. The "schema" is actually just a pyhton code expression that evaluates to a boolean validation function. It's fairly minimal, so simply copying python_data_schema.py into your project should work.

The modular set of function-returning functions that is this library may be used to create a function that validates some data (typically before inserting it into a database). For example, a validation function for a MongoDB collection can be created by defining a list of dictionaries. Take a look at example.py for a complete example.

A "validation function" (or "validator") is a function that takes one argument, which is data to be validated, and returns a boolean value.

A "validator generator" is a function that returns a validation function. (Ex. ```equals_()```, ```and_()```) (These are not generators in the Python sense of the word, only in the sense that they generate another function)

Basic example:
```python
# ValidatorFunction = validatorGenerator(value)
is_a_string = type_is_(str)
print(is_a_string("indeed")) # True
```

Combine validators with the validator generators ```and_()``` and ```or_()```:
```python
is_primary_color = and_([
  type_is_(str),
  or_([
    equals_("red"),
    equals_("green"),
    lambda data: data == "blue" # same as equals_("blue")
  ])
])
print(is_primary_color("red"), is_primary_color("cyan")) # True False
```

Defining a list using ```for_each_item_()```:
```python
# note: and_(v1, v2, v3) == and_([v1, v2, v3])
is_list_of_ints = and_(type_is_(list), for_each_item_(type_is_(int)))
print(is_list_of_ints([1, 2, 3, "Sam"])) # False
```

Defining a dictionary using ```for_each_item_()``` and ```or_()```:
```python
short_or_syntax = or_({
    # key validator: value validator
    "sequence": type_is_(str), # "sequence" is short for equals_("sequence")
    "hydrophobicity": (lambda data_value: type(data_value) is float)
})
long_or_syntax = or_([
    and_([
        key(equals_("sequence")),
        value(type_is_(str))
    ]),
    and_([
        lambda key,value: key == "hydrophobicity",
        lambda key,value: type(value) is float
    ])
])
print(short_or_syntax.__code__.co_code == long_or_syntax.__code__.co_code) # True
# note: there is no short and_() syntax, only or_() may take a dict as an arg

dict_validator = and_(type_is_(dict), for_each_item_(short_or_syntax))
test_data = {"sequence": "FLPAIAGILSQLF", "hydrophobicity": 0.769231}
print(dict_validator(test_data)) # True
```
Note: Any function that takes multiple arguments may also take a list of arguments

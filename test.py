import unittest
from example import test_data, mongo_collection_validator

class TestDataSchema(unittest.TestCase):
    def test_validity_of_example_schema(self):
        self.assertTrue( mongo_collection_validator(test_data) )

    def test_validity_of_invalid_schema(self):
        test_data[0]["sequence"] = 74
        self.assertFalse( mongo_collection_validator(test_data) )

if __name__ == '__main__':
    unittest.main()

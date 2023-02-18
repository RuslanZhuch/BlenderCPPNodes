import unittest

import json

from os import path
import sys
 

from pathlib import Path
root_dir = Path.cwd()
sys.path.append(root_dir)

import cpp_generator

class TestCppGenerator(unittest.TestCase):

    def test_gen_high_level_signature_1(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        signature = cpp_generator.generate_signature(schema)
        self.assertEqual(signature, "auto code(auto&& arg1)")
        schema_file.close()

    def test_gen_high_level_signature_2(self):
        schema_file = open("tests\\resources\\nodes_2_schema.json")
        schema = json.load(schema_file)
        signature = cpp_generator.generate_signature(schema)
        self.assertEqual(signature, "auto code(auto&& arg1, auto&& arg2)")
        schema_file.close()

if __name__ == '__main__':
    unittest.main()
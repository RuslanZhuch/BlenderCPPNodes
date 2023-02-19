import unittest

import json

from os import path
import sys
 

from pathlib import Path
root_dir = Path.cwd()
sys.path.append(root_dir)

import cpp_generator

def gather_node_data_input(schema_data):
    data = schema_data["data"]
    node_data = None
    for node in data:
        if node["name"] == "Input":
            return node    

def gather_node_data_output(schema_data):
    data = schema_data["data"]
    node_data = None
    for node in data:
        if node["name"] == "Output":
            return node 
        
class TestCppGenerator(unittest.TestCase):

    def test_gather_node_data(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        self.assertEqual(cpp_generator.gather_node_data(schema, "Input"), gather_node_data_input(schema))
        self.assertEqual(cpp_generator.gather_node_data(schema, "Output"), gather_node_data_output(schema))
        schema_file.close()

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

    def test_gen_args_for_schema2_and(self):
        schema_file = open("tests\\resources\\nodes_2_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "and")
        generated = cpp_generator.generate_call_args(function_schema)
        self.assertEqual(generated, "arg1, arg2")
        schema_file.close()

    def test_gen_schema1_not_function_call(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "not")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const decltype(auto) notResult{ not(arg1) };")
        schema_file.close()

if __name__ == '__main__':
    unittest.main()
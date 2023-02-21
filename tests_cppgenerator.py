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

    def test_gen_output_list_schema1(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate_output_list(schema)
        self.assertEqual(generated, ["notResult"])
        schema_file.close()

    def test_gen_output_list_schema2(self):
        schema_file = open("tests\\resources\\nodes_2_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate_output_list(schema)
        self.assertEqual(generated, ["andResult", "orResult"])
        schema_file.close()

    def test_gen_return(self):
        generated1 = cpp_generator.generate_return_from_list(["notResult"])
        self.assertEqual(generated1, "return { notResult };")

        generated2 = cpp_generator.generate_return_from_list(["andResult", "orResult"])
        self.assertEqual(generated2, "return { andResult, orResult };")

    def test_gen_tabulation(self):
        self.assertEqual(cpp_generator.tabulate("some string", 0), "some string")
        self.assertEqual(cpp_generator.tabulate("some string"), "    some string")
        self.assertEqual(cpp_generator.tabulate("some string", 1), "    some string")
        self.assertEqual(cpp_generator.tabulate("some string", 2), "        some string")
        self.assertEqual(cpp_generator.tabulate("some string", 3), "            some string")

    def test_gen_scope(self):
        ctx = cpp_generator.Context()

        self.assertEqual(cpp_generator.put_line("Line 1", ctx), "Line 1")
        self.assertEqual(cpp_generator.put_line("Line 2", ctx), "Line 2") 
        self.assertEqual(cpp_generator.push_scope(ctx), "{")
        self.assertEqual(cpp_generator.put_line("Line 3", ctx), "    Line 3") 
        self.assertEqual(cpp_generator.put_line("Line 4", ctx), "    Line 4") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "}")
        self.assertEqual(cpp_generator.put_line("Line 5", ctx), "Line 5")
        self.assertEqual(cpp_generator.put_line("Line 6", ctx), "Line 6") 

    def test_gen_scope_nested(self):
        ctx = cpp_generator.Context()
        self.assertEqual(cpp_generator.push_scope(ctx), "{")
        self.assertEqual(cpp_generator.put_line("Line 1", ctx), "    Line 1") 
        self.assertEqual(cpp_generator.push_scope(ctx), "    {")
        self.assertEqual(cpp_generator.put_line("Line 2", ctx), "        Line 2") 
        self.assertEqual(cpp_generator.push_scope(ctx), "        {")
        self.assertEqual(cpp_generator.put_line("Line 3", ctx), "            Line 3") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "        }")
        self.assertEqual(cpp_generator.put_line("Line 4", ctx), "        Line 4") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "    }")
        self.assertEqual(cpp_generator.put_line("Line 5", ctx), "    Line 5") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "}")
        self.assertEqual(cpp_generator.put_line("Line 6", ctx), "Line 6") 


if __name__ == '__main__':
    unittest.main()
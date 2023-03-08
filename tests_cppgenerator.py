import unittest

import json

from os import path
import sys
 

from pathlib import Path
root_dir = Path.cwd()
sys.path.append(root_dir)

import cpp_generator
import nodes_meta

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

    def test_name_correction(self):
        self.assertEqual(cpp_generator.correct_name("name.001"), "name_001")
        self.assertEqual(cpp_generator.correct_name("name2.002"), "name2_002")
        self.assertEqual(cpp_generator.correct_name("name3."), "name3_")
        self.assertEqual(cpp_generator.correct_name(".name"), "_name")
        self.assertEqual(cpp_generator.correct_name("."), "_")

    def test_gen_high_level_signature_1(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        signature = cpp_generator.generate_signature(schema)
        self.assertEqual(signature, "auto schema_1(auto&& arg1)")
        schema_file.close()

    def test_gen_high_level_signature_2(self):
        schema_file = open("tests\\resources\\nodes_2_schema.json")
        schema = json.load(schema_file)
        signature = cpp_generator.generate_signature(schema)
        self.assertEqual(signature, "auto schema_2(auto&& arg1, auto&& arg2)")
        schema_file.close()

    def test_gen_args_for_schema2_and(self):
        schema_file = open("tests\\resources\\nodes_2_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "and")
        generated = cpp_generator.generate_call_args(function_schema)
        self.assertEqual(generated, "arg1, arg2")
        schema_file.close()

    def test_gen_args_for_schema3_and(self):
        schema_file = open("tests\\resources\\nodes_3_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "and")
        generated = cpp_generator.generate_call_args(function_schema)
        self.assertEqual(generated, "notResult, arg1")
        schema_file.close()

    def test_gen_schema1_not_function_call(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "not")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const auto notResult{ Blocks::Binary::not(arg1) };")
        schema_file.close()

    def test_gen_schema5_stretch_function_call(self):
        schema_file = open("tests\\resources\\nodes_5_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "stretch")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const auto stretchResult{ Blocks::MultiOutput::stretch(arg1) };")
        schema_file.close()

    def test_gen_schema5_Vec2_call(self):
        schema_file = open("tests\\resources\\nodes_5_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "Vec2")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const auto [ Vec2x, Vec2y ]{ Types::Vec2(stretchResult) };")
        schema_file.close()

    def test_gen_schema6_not_001_call(self):
        schema_file = open("tests\\resources\\nodes_6_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "not.001")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const auto not_001Result{ Blocks::Binary::not_001(arg1) };")
        schema_file.close()

    def test_gen_schema6_not_002_call(self):
        schema_file = open("tests\\resources\\nodes_6_schema.json")
        schema = json.load(schema_file)
        function_schema = cpp_generator.gather_node_data(schema, "not.002")
        generated = cpp_generator.generate_function_call(function_schema)
        self.assertEqual(generated, "const auto not_002Result{ Blocks::Binary::not_002(not_001Result) };")
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
        
    def test_gen_output_list_schema5(self):
        schema_file = open("tests\\resources\\nodes_5_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate_output_list(schema)
        self.assertEqual(generated, ["Vec2x", "Vec2y"])
        schema_file.close()
        
    def test_gen_output_list_schema6(self):
        schema_file = open("tests\\resources\\nodes_6_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate_output_list(schema)
        self.assertEqual(generated, ["not_002Result"])
        schema_file.close()

    def test_gen_return(self):
        ctx = cpp_generator.Context()
        generated1 = cpp_generator.generate_return_from_list(["notResult"], ctx)
        self.assertEqual(generated1, "struct OutS\n{\n    decltype(notResult) out1;\n};\nreturn OutS(notResult);\n")

        generated2 = cpp_generator.generate_return_from_list(["andResult", "orResult"], ctx)
        self.assertEqual(generated2, "struct OutS\n{\n    decltype(andResult) out1;\n    decltype(orResult) out2;\n};\nreturn OutS(andResult, orResult);\n")

    def test_gen_tabulation(self):
        self.assertEqual(cpp_generator.tabulate("some string", 0), "some string")
        self.assertEqual(cpp_generator.tabulate("some string"), "    some string")
        self.assertEqual(cpp_generator.tabulate("some string", 1), "    some string")
        self.assertEqual(cpp_generator.tabulate("some string", 2), "        some string")
        self.assertEqual(cpp_generator.tabulate("some string", 3), "            some string")

    def test_gen_scope(self):
        ctx = cpp_generator.Context()

        self.assertEqual(cpp_generator.put_line("Line 1", ctx), "Line 1\n")
        self.assertEqual(cpp_generator.put_line("Line 2", ctx), "Line 2\n") 
        self.assertEqual(cpp_generator.push_scope(ctx), "{\n")
        self.assertEqual(cpp_generator.put_line("Line 3", ctx), "    Line 3\n") 
        self.assertEqual(cpp_generator.put_line("Line 4", ctx), "    Line 4\n") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "}\n")
        self.assertEqual(cpp_generator.put_line("Line 5", ctx), "Line 5\n")
        self.assertEqual(cpp_generator.put_line("Line 6", ctx), "Line 6\n")
        self.assertEqual(cpp_generator.push_scope(ctx), "{\n")
        self.assertEqual(cpp_generator.put_line("Line 7", ctx), "    Line 7\n")
        self.assertEqual(cpp_generator.pull_scope(ctx, semi=True), "};\n")
        self.assertEqual(cpp_generator.put_line("Line 8", ctx), "Line 8\n")

    def test_gen_scope_nested(self):
        ctx = cpp_generator.Context()

        self.assertEqual(cpp_generator.push_scope(ctx), "{\n")
        self.assertEqual(cpp_generator.put_line("Line 1", ctx), "    Line 1\n") 
        self.assertEqual(cpp_generator.push_scope(ctx), "    {\n")
        self.assertEqual(cpp_generator.put_line("Line 2", ctx), "        Line 2\n") 
        self.assertEqual(cpp_generator.push_scope(ctx), "        {\n")
        self.assertEqual(cpp_generator.put_line("Line 3", ctx), "            Line 3\n") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "        }\n")
        self.assertEqual(cpp_generator.put_line("Line 4", ctx), "        Line 4\n") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "    }\n")
        self.assertEqual(cpp_generator.put_line("Line 5", ctx), "    Line 5\n") 
        self.assertEqual(cpp_generator.pull_scope(ctx), "}\n")
        self.assertEqual(cpp_generator.put_line("Line 6", ctx), "Line 6\n") 

    def test_gen_schema1(self):
        schema_file = open("tests\\resources\\nodes_1_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate(schema)
        expected_file = open("tests\\resources\\nodes_1_generated.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()
        schema_file.close()
        
    def test_gen_schema3(self):
        schema_file = open("tests\\resources\\nodes_3_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate(schema)
        expected_file = open("tests\\resources\\nodes_3_generated.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()
        schema_file.close()
        
    def test_gen_schema4(self):
        schema_file = open("tests\\resources\\nodes_4_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate(schema)
        expected_file = open("tests\\resources\\nodes_4_generated.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()
        schema_file.close()
        
    def test_gen_schema5(self):
        schema_file = open("tests\\resources\\nodes_5_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate(schema)
        expected_file = open("tests\\resources\\nodes_5_generated.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()
        schema_file.close()
        
    def test_gen_schema6(self):
        schema_file = open("tests\\resources\\nodes_6_schema.json")
        schema = json.load(schema_file)
        generated = cpp_generator.generate(schema)
        expected_file = open("tests\\resources\\nodes_6_generated.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()
        schema_file.close()

    def test_gen_cpp_from_schema_1(self):
        generated_result = cpp_generator.generate_cpp("tests\\resources\\nodes_1_schema.json", "tests\\resources\\generated")
        self.assertTrue(generated_result)
        expected_file = open("tests\\resources\\nodes_1_generated.h", 'r')
        generated_file = open("tests\\resources\\generated\\nodes_1_schema.h", 'r')
        
        self.assertEqual(expected_file.read(), generated_file.read())

        expected_file.close()
        generated_file.close()

    def test_gen_cpp_from_schema_3(self):
        generated_result = cpp_generator.generate_cpp("tests\\resources\\nodes_3_schema.json", "tests\\resources\\generated")
        self.assertTrue(generated_result)
        expected_file = open("tests\\resources\\nodes_3_generated.h", 'r')
        generated_file = open("tests\\resources\\generated\\nodes_3_schema.h", 'r')
        
        self.assertEqual(expected_file.read(), generated_file.read())

        expected_file.close()
        generated_file.close()

    def test_gen_includes_content(self):
        generated = cpp_generator.generate_includes([
            "include_1.h", 
            "include_2.h", 
            "include_3.h", 
            "include_4.h", 
            "include_5.h", 
            ])
        expected_file = open("tests\\resources\\expected_includes.h", 'r')
        self.assertEqual(generated, expected_file.read())
        expected_file.close()

    def test_gen_includes_file(self):
        cpp_generator.generate_includes_file([
            "include_1.h", 
            "include_2.h", 
            "include_3.h", 
            "include_4.h", 
            "include_5.h", 
            ], "tests\\resources\\generated")
        expected_file = open("tests\\resources\\expected_includes.h", 'r')
        generated_file = open("tests\\resources\\generated\\generationIncludes.h", 'r')
        
        self.assertEqual(expected_file.read(), generated_file.read())

        expected_file.close()
        generated_file.close()
import json

class Context:
    def __init__(self):
        self.tab_level = 0


def gather_node_data(schema, node_name):
    data = schema["data"]
    for node in data:
        if node["name"] == node_name:
            return node

    return None

def generate_signature(schema):
    def generate_arguments(schema):
        args = ""
        data = schema["data"]
        node_data = gather_node_data(schema, "Input")
        
        outputs_schema = node_data["outputsSchema"]
        outputs_names = outputs_schema["names"]
        num_of_args = len(outputs_names) - 1

        for arg_id in range(0, num_of_args):
            if arg_id > 0:
                args += ", "
            args += "auto&& arg{}".format(arg_id + 1)

        return args

    args = generate_arguments(schema)
    return "auto {}({})".format(schema["name"], args)

def generate_call_args(function_schema):
    inputs = function_schema["inputs"]
    args = []
    for input_data in inputs:
        if input_data["target_node_name"] == "Input":
            args.append("arg{}".format(input_data["target_socket_id"] + 1))
        else:
            args.append("{}Result".format(input_data["target_node_name"]))
    
    args_string = ""
    for arg in args:
        if arg != args[0]:
            args_string += ", "
        args_string += arg

    return args_string

def generate_function_call(function_schema):
    def gen_call_body_str():
        return "{}({})".format(
            function_schema["name"],
            generate_call_args(function_schema)
        )

    outputs_schema = function_schema["outputsSchema"]
    output_names = outputs_schema["names"]
    if len(output_names) == 1:
        return "const auto {}Result{{ {} }};".format(
            function_schema["name"],
            gen_call_body_str()
        )

    function_name = function_schema["name"]
    output_full_names = list(map(lambda name: "{}{}".format(function_name, name), output_names))
    output_full_names_parsed = ""
    for output_full_name in output_full_names:
        if output_full_name != output_full_names[0]:
            output_full_names_parsed += ", "
        output_full_names_parsed += output_full_name

    return "const auto [ {} ]{{ {} }};".format(
        output_full_names_parsed,
        gen_call_body_str()
    )

def generate_output_list(schema):
    node = gather_node_data(schema, "Output")
    inputs = node["inputs"]

    inputs_list = []
    for input_data in inputs:
        source_node_name = input_data["target_node_name"]
        source_node = gather_node_data(schema, source_node_name)
        outputsSchema = source_node["outputsSchema"]
        source_outputs = outputsSchema["names"]
        source_output_id = input_data["target_socket_id"]
        
        inputs_list.append("{}{}".format(source_node_name, source_outputs[source_output_id]))
    
    return inputs_list

def generate_return_from_list(inputs_list):
    output_names = ""
    for input_name in inputs_list:
        if input_name != inputs_list[0]:
            output_names += ", "
        output_names += input_name

    return "return {{ {} }};".format(output_names)

def tabulate(input_string, level = 1):
    tabs_str = ""
    for _ in range(0, level):
        tabs_str += "    "
    return "{}{}".format(tabs_str, input_string)

def put_line(line, context):
    return "{}\n".format(tabulate(line, context.tab_level))

def push_scope(context):
    output_str = tabulate("{\n", context.tab_level)
    context.tab_level += 1
    return output_str

def pull_scope(context):
    context.tab_level -= 1
    return tabulate("}\n", context.tab_level)

def generate(schema):
    context = Context()

    file_data = put_line(generate_signature(schema), context)
    file_data += push_scope(context)

    schema_data = schema["data"]
    for node_data in reversed(schema_data):
        node_name = node_data["name"]
        if node_name != "Output" and node_name != "Input":
            call_str = generate_function_call(node_data)
            file_data += put_line(call_str, context)

    file_data += put_line(generate_return_from_list(generate_output_list(schema)), context)

    file_data += pull_scope(context)
    return file_data
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
    return "auto code({})".format(args)

def generate_call_args(function_schema):
    inputs = function_schema["inputs"]
    args = []
    for input_data in inputs:
        if input_data["target_node_name"] == "Input":
            args.append("arg{}".format(input_data["target_socket_id"] + 1))
    
    args_string = ""
    for arg in args:
        if arg != args[0]:
            args_string += ", "
        args_string += arg

    return args_string

def generate_function_call(function_schema):
    return "const decltype(auto) {}Result{{ {} }};".format(
        function_schema["name"],
        "{}({})".format(
            function_schema["name"],
            generate_call_args(function_schema)
        )
    )

def generate_output_list(schema):
    node = gather_node_data(schema, "Output")
    inputs = node["inputs"]

    inputs_list = []
    for input_data in inputs:
        inputs_list.append(input_data["target_node_name"] + "Result")
    
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
    return tabulate(line, context.tab_level)

def push_scope(context):
    output_str = tabulate("{", context.tab_level)
    context.tab_level += 1
    return output_str

def pull_scope(context):
    context.tab_level -= 1
    return tabulate("}", context.tab_level)
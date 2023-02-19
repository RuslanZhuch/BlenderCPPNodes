import json


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

import json

def generate_signature(schema):
    def generate_arguments(schema):
        args = ""
        data = schema["data"]
        node_data = None
        for node in data:
            if node["name"] == "Input":
                node_data = node
                break
        
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

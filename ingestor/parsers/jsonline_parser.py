import ast


def parse_jsonline(log_line):
    try:
        return ast.literal_eval(log_line)
    except Exception as e:
        print(f"Error parsing JSON line: {e}")
        return None
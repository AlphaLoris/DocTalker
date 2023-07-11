import os
import ast
import sys


def get_module_path(import_name, current_path):
    """
    Given a module's import name, returns its path
    """
    for top, dirs, files in os.walk(os.path.dirname(current_path)):
        for filename in files:
            if filename == f"{import_name}.py":
                return os.path.join(top, filename)
    return None


def aggregate_code(filename, visited_files):
    """
    Aggregate code from the Python file and its dependencies
    """
    with open(filename, 'r') as file:
        tree = ast.parse(file.read())
        aggregated_code = ""

        # Import modules are handled in a DFS manner
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_path = get_module_path(alias.name, filename)
                    if module_path and module_path not in visited_files:
                        visited_files.add(module_path)
                        aggregated_code += aggregate_code(module_path, visited_files)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:  # global import
                    module_path = get_module_path(node.module, filename)
                    if module_path and module_path not in visited_files:
                        visited_files.add(module_path)
                        aggregated_code += aggregate_code(module_path, visited_files)

        # Add the current file code
        aggregated_code += '\n# File: ' + filename + '\n'
        with open(filename, "r") as f:
            aggregated_code += f.read()

    return aggregated_code


def main(start_file, output_filename):
    visited_files = set()
    aggregated_code = aggregate_code(start_file, visited_files)

    with open(output_filename, "w") as output_file:
        output_file.write(aggregated_code)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

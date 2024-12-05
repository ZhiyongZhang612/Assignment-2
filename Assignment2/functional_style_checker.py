import ast
import os
import re

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    non_empty_lines = [line for line in lines if line.strip() != '']
    return f"Total number of lines: {len(non_empty_lines)}\n"

def check_imports(tree):
    imports = [node for node in tree.body if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
    result = "Imports:\n"
    for imp in imports:
        if isinstance(imp, ast.Import):
            result += ", ".join([alias.name for alias in imp.names]) + "\n"
        elif isinstance(imp, ast.ImportFrom):
            result += f"{imp.module}\n"
    return result

def check_classes(tree):
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    result = "Classes:\n"
    for cls in classes:
        result += f"{cls.name}\n"
    return result

def check_functions(tree):
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and not any((isinstance(parent, ast.ClassDef) for parent in ast.walk(node)))]
    result = "Functions:\n"
    for func in functions:
        result += f"{func.name}\n"
    return result

def check_docstrings(tree):
    result = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                result += f"{node.name}: DocString not found.\n"
            else:
                result += f"{node.name}:{ast.get_docstring(node)} + \n"
    return result

def check_type_annotations(tree):
    result = ""
    has_type_annotations = all(any(isinstance(arg, ast.arg) and arg.annotation for arg in node.args.args) for node in tree.body if isinstance(node, ast.FunctionDef))
    if not has_type_annotations:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not any(isinstance(arg, ast.arg) and arg.annotation for arg in node.args.args):
                result += f"Function {node.name} does not use type annotations.\n"
    else:
        result += "Type annotation is used in all functions and methods"
    return result

def check_naming_conventions(tree):
    result = ""
    naming_conventions_followed = True
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            pattern = re.compile("^[A-Z][a-zA-Z]*$")
            if not pattern.match(node.name):
                result += f"Class {node.name} does not follow CamelCase naming convention.\n"
                naming_conventions_followed = False
        elif isinstance(node, ast.FunctionDef):
            pattern = re.compile("^[a-z][a-z_]*$")
            if not pattern.match(node.name):
                result += f"Function {node.name} does not follow lower_case_with_underscores naming convention.\n"
                naming_conventions_followed = False
    if naming_conventions_followed:
        result += "All names adhere to the specified naming convention"
    return result

def analyze_tree(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    return (
        count_lines(file_path) +
        check_imports(tree) +
        check_classes(tree) +
        check_functions(tree) +
        check_docstrings(tree) +
        check_type_annotations(tree) +
        check_naming_conventions(tree)
    )

def save_report(file_path, content):
    report_path = f"style_report_{os.path.basename(file_path)}.txt"
    with open(report_path, 'w') as report_file:
        report_file.write(content)

def check_style(file_path):
    content = analyze_tree(file_path)
    save_report(file_path, content)

if __name__ == "__main__":
    check_style('test.py')
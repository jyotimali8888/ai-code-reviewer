from pathlib import Path
import ast


# --------------------------------
# Parse Python file
# --------------------------------

def parse_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    return ast.parse(code)


# --------------------------------
# Analyze Python file
# --------------------------------

def analyze_python_file(file_path):
    tree = parse_python_file(file_path)

    functions = []
    classes = []
    imports = []
    long_functions = []
    missing_docstrings = []

    for node in ast.walk(tree):

        # Find functions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

            # Check function length
            if node.end_lineno is not None:
                lines = node.end_lineno - node.lineno + 1

                if lines > 30:
                    long_functions.append({
                        "name": node.name,
                        "lines": lines
                    })

            # Check for missing docstring
            if ast.get_docstring(node) is None:
                missing_docstrings.append(node.name)

        # Find classes
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        # Find normal imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        # Find from ... import ...
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "file": str(file_path),
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "long_functions": long_functions,
        "missing_docstrings": missing_docstrings,
    }


# --------------------------------
# Get project name
# --------------------------------

def get_project_name(root):
    return root.resolve().name


# --------------------------------
# Count folders
# --------------------------------

def count_folders(root, ignore):
    count = 0

    for item in root.rglob("*"):

        if item.is_dir():

            if any(part in ignore for part in item.parts):
                continue

            count += 1

    return count


# --------------------------------
# Calculate project size
# --------------------------------

def calculate_size(root, ignore):
    total_size = 0

    for item in root.rglob("*"):

        if any(part in ignore for part in item.parts):
            continue

        if item.is_file():
            total_size += item.stat().st_size

    return round(total_size / 1024, 2)


# --------------------------------
# Scan repository
# --------------------------------

def scan_repository(path: str):
    root = Path(path)

    ignore = {
        ".git",
        ".venv",
        "__pycache__",
    }

    python_files = 0
    markdown_files = 0
    text_files = 0
    other_files = 0

    python_analysis = []

    for item in root.rglob("*"):

        if any(part in ignore for part in item.parts):
            continue

        if item.is_file():

            if item.suffix == ".py":
                python_files += 1

                try:
                    analysis = analyze_python_file(item)
                    python_analysis.append(analysis)

                except SyntaxError:
                    python_analysis.append({
                        "file": str(item),
                        "functions": [],
                        "classes": [],
                        "imports": [],
                        "long_functions": [],
                        "missing_docstrings": [],
                        "error": "Syntax error"
                    })

            elif item.suffix == ".md":
                markdown_files += 1

            elif item.suffix == ".txt":
                text_files += 1

            else:
                other_files += 1

    return {
        "project_name": get_project_name(root),
        "folders": count_folders(root, ignore),
        "size_kb": calculate_size(root, ignore),
        "python": python_files,
        "markdown": markdown_files,
        "text": text_files,
        "other": other_files,
        "python_analysis": python_analysis,
    }


# --------------------------------
# Test analyzer directly
# --------------------------------

if __name__ == "__main__":
    result = analyze_python_file("app/main.py")
    print(result)
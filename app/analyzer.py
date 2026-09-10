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
# Calculate code quality score
# --------------------------------

def calculate_quality_score(analysis):
    score = 100

    score -= len(analysis["long_functions"]) * 5
    score -= len(analysis["missing_docstrings"]) * 2
    score -= len(analysis["unused_imports"]) * 3
    score -= len(analysis["complex_functions"]) * 5
    score -= len(analysis["security_issues"]) * 10

    return max(score, 0)
# --------------------------------
# Detect duplicate functions
# --------------------------------

def find_duplicate_functions(tree):
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            # Create a copy of the function
            function_copy = ast.FunctionDef(
                name="function",
                args=node.args,
                body=node.body,
                decorator_list=[],
                returns=node.returns,
            )

            # Convert the function structure to text
            source = ast.dump(
                function_copy,
                annotate_fields=False,
                include_attributes=False,
            )

            functions.append({
                "name": node.name,
                "source": source,
                "line": node.lineno,
            })

    duplicates = []

    for i in range(len(functions)):
        for j in range(i + 1, len(functions)):

            if functions[i]["source"] == functions[j]["source"]:
                duplicates.append({
                    "function1": functions[i]["name"],
                    "function2": functions[j]["name"],
                    "line1": functions[i]["line"],
                    "line2": functions[j]["line"],
                })

    return duplicates
# --------------------------------
# Analyze Python file
# --------------------------------
def calculate_complexity(function_node):
    complexity = 1

    for node in ast.walk(function_node):

        if isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.Try,
                ast.ExceptHandler,
                ast.With,
                ast.IfExp,
            ),
        ):
            complexity += 1

        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1

    return complexity
def analyze_python_file(file_path):
    tree = parse_python_file(file_path)
    duplicates = find_duplicate_functions(tree)

    functions = []
    classes = []
    imports = []
    long_functions = []
    complex_functions = []
    missing_docstrings = []
    unused_imports = []
    security_issues = []
    used_names = set()

    # Find functions, classes, imports, and security issues
    for node in ast.walk(tree):

        # Find functions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
                        # Check cyclomatic complexity
            complexity = calculate_complexity(node)

            if complexity > 10:
                complex_functions.append({
                    "name": node.name,
                    "complexity": complexity
                })
            # Check function length
            if node.end_lineno is not None:
                lines = node.end_lineno - node.lineno + 1

                if lines > 30:
                    long_functions.append({
                        "name": node.name,
                        "lines": lines
                    })

            # Check missing docstring
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

        # Detect potentially dangerous functions
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in {"eval", "exec"}:
                    security_issues.append({
                        "name": node.func.id,
                        "line": node.lineno
                    })

    # Find names actually used in code
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Find unused imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = (
                    alias.asname
                    if alias.asname
                    else alias.name.split(".")[0]
                )

                if name not in used_names:
                    unused_imports.append(name)

    return {
        "file": str(file_path),
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "long_functions": long_functions,
        "complex_functions": complex_functions,
        "missing_docstrings": missing_docstrings,
        "unused_imports": unused_imports,
        "security_issues": security_issues,
        "duplicates": duplicates,
        "quality_score": calculate_quality_score({
            "long_functions": long_functions,
            "missing_docstrings": missing_docstrings,
            "unused_imports": unused_imports,
            "complex_functions": complex_functions,
            "security_issues": security_issues,
        }),
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

                except SyntaxError as error:
                    python_analysis.append({
                        "file": str(item),
                        "functions": [],
                        "classes": [],
                        "imports": [],
                        "long_functions": [],
                        "missing_docstrings": [],
                        "unused_imports": [],
                        "security_issues": [],
                        "error": {
                            "message": error.msg,
                            "line": error.lineno,
                            "column": error.offset
                        }
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
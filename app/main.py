import typer
from rich.console import Console

from analyzer import scan_repository

app = typer.Typer()
console = Console()


@app.command()
def review(path: str):
    console.print(f"[green]Scanning repository:[/green] {path}")

    result = scan_repository(path)

    console.print()

    console.print(f"Project Name : {result['project_name']}")
    console.print(f"Folders      : {result['folders']}")
    console.print(f"Size (KB)    : {result['size_kb']}")

    console.print()

    console.print(f"Python files   : {result['python']}")
    console.print(f"Markdown files : {result['markdown']}")
    console.print(f"Text files     : {result['text']}")
    console.print(f"Other files    : {result['other']}")

    console.print()
    console.print("Python Code Analysis")

    for analysis in result["python_analysis"]:
        console.print()
        console.print(analysis["file"])

        functions = (
            ", ".join(analysis["functions"])
            if analysis["functions"]
            else "None"
        )

        classes = (
            ", ".join(analysis["classes"])
            if analysis["classes"]
            else "None"
        )

        imports = (
            ", ".join(analysis["imports"])
            if analysis["imports"]
            else "None"
        )

        console.print(f"  Functions : {functions}")
        console.print(f"  Classes   : {classes}")
        console.print(f"  Imports   : {imports}")

        for item in analysis["long_functions"]:
            console.print(
                f"  [yellow]⚠ Long function: {item['name']} "
                f"({item['lines']} lines)[/yellow]"
            )

        for name in analysis["missing_docstrings"]:
            console.print(
                f"  [yellow]⚠ Missing docstring: {name}[/yellow]"
            )

        for name in analysis["unused_imports"]:
            console.print(
                f"  [red]⚠ Unused import: {name}[/red]"
            )
        for issue in analysis["security_issues"]:
            console.print(
                f"  [red]🔴 Security issue: {issue['name']}() "
                f"at line {issue['line']}[/red]"
            )

        if "error" in analysis:
            error = analysis["error"]

            console.print(
                f"  [red]⚠ Syntax error: {error['message']}[/red]"
            )

            console.print(
                f"  [red]  Line: {error['line']} "
                f"Column: {error['column']}[/red]"
            )


if __name__ == "__main__":
    app()
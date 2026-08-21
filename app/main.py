import typer
from rich.console import Console

from analyzer import scan_repository


app = typer.Typer()
console = Console()


@app.command()
def review(path: str):

    console.print(
        f"[green]Scanning repository:[/green] {path}"
    )

    result = scan_repository(path)

    console.print()

    # --------------------------------
    # Repository information
    # --------------------------------

    console.print(
        f"Project Name : {result['project_name']}"
    )

    console.print(
        f"Folders      : {result['folders']}"
    )

    console.print(
        f"Size (KB)    : {result['size_kb']}"
    )

    console.print()

    console.print(
        f"Python files   : {result['python']}"
    )

    console.print(
        f"Markdown files : {result['markdown']}"
    )

    console.print(
        f"Text files     : {result['text']}"
    )

    console.print(
        f"Other files    : {result['other']}"
    )

    # --------------------------------
    # Python Code Analysis
    # --------------------------------

    console.print()
    console.print("[bold blue]Python Code Analysis[/bold blue]")
    console.print()

    for analysis in result["python_analysis"]:

        console.print(analysis["file"])

        console.print(
            f"  Functions : "
            f"{', '.join(analysis['functions']) if analysis['functions'] else 'None'}"
        )

        console.print(
            f"  Classes   : "
            f"{', '.join(analysis['classes']) if analysis['classes'] else 'None'}"
        )

        console.print(
            f"  Imports   : "
            f"{', '.join(analysis['imports']) if analysis['imports'] else 'None'}"
        )

        # --------------------------------
        # Long function warnings
        # --------------------------------

        for function in analysis["long_functions"]:

            console.print(
                f"  [yellow]⚠ Long function:[/yellow] "
                f"{function['name']} "
                f"({function['lines']} lines)"
            )

        # --------------------------------
        # Missing docstring warnings
        # --------------------------------

        for function_name in analysis["missing_docstrings"]:

            console.print(
                f"  [yellow]⚠ Missing docstring:[/yellow] "
                f"{function_name}"
            )

        console.print()


if __name__ == "__main__":
    app()
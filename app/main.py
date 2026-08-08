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

    console.print("[bold cyan]Python Code Analysis[/bold cyan]")

    for analysis in result["python_analysis"]:
        console.print(f"\n[bold]{analysis['file']}[/bold]")

        if analysis["functions"]:
            console.print(
                f"  Functions : {', '.join(analysis['functions'])}"
            )
        else:
            console.print("  Functions : None")

        if analysis["classes"]:
            console.print(
                f"  Classes   : {', '.join(analysis['classes'])}"
            )
        else:
            console.print("  Classes   : None")

        if analysis["imports"]:
            console.print(
                f"  Imports   : {', '.join(analysis['imports'])}"
            )
        else:
            console.print("  Imports   : None")


if __name__ == "__main__":
    app()
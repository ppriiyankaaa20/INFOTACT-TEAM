import typer
from main import PyChronicle

app = typer.Typer()


@app.command()
def run(filename: str):
    """
    Run PyChronicle on a Python file.
    """
    project = PyChronicle(filename)
    project.run()
    project.close()


@app.command()
def version():
    """
    Show version.
    """
    print("PyChronicle Version 1.0")


if __name__ == "__main__":
    app()
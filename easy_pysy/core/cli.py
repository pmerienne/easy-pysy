import typer
from easy_pysy.core.lifecycle import start, context, AppState

main_typer = typer.Typer()
# main_typer.add_typer(run_typer, name="run")

command = main_typer.command


def run(auto_start=True):
    if auto_start and context.state == AppState.STOPPED:
        start()
    main_typer()

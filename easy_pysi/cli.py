import typer

main_typer = typer.Typer()
# main_typer.add_typer(run_typer, name="run")

command = main_typer.command
run_cli = main_typer

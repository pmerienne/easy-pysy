import typer

from easy_pysy import current_app
from examples.petclinic.services import OwnerService

crud_cli = typer.Typer(name='crud')


@crud_cli.command()
def list_owners():
    app = current_app()
    with app:  # Start and stop app with a context manager
        owners = app.get(OwnerService)
        for owner in owners.find_all():
            print(f'- {owner}')

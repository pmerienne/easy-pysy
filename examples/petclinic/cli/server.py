import typer
import uvicorn

server_cli = typer.Typer(name='server')


@server_cli.command()
def start(host: str = '0.0.0.0', port: int = 5000, reload: bool = True):
    uvicorn.run('app:app.fast_api', host=host, port=port, reload=reload)

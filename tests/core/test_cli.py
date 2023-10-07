from pydantic import Field
from typer import Typer
from typer.testing import CliRunner

from easy_pysy import EzApp, inject, Singleton
from easy_pysy.plugins.cli import CLI


class MessageBox(Singleton):
    messages: list[str] = Field(default_factory=list)


box_cli = Typer(name='box')


@box_cli.command()
def add(message: str):
    box = inject(MessageBox)
    box.messages.append(message)


def test_run():
    with EzApp(components=[MessageBox], cli=CLI(clis=[box_cli])) as app:
        runner = CliRunner()
        runner.invoke(app.cli.root_cli, ['box', 'add', 'hello'])  # Works
        # app.run('box add hello')  TODO: don't work in test !
        runner.invoke(app.cli.root_cli, ['box', 'add', 'you'])
        assert app.get(MessageBox).messages == ['hello', 'you']

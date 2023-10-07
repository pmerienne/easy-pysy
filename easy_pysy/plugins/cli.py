from pydantic import BaseModel, Field
from typer import Typer


class CLI(BaseModel):
    clis: list[Typer] = Field(default_factory=[])  # TODO: dict with name
    root_cli: Typer = Field(default_factory=Typer)

    def __init__(self, **data):
        super().__init__(**data)

        for cli in self.clis:
            self.root_cli.add_typer(cli)

    def run(self, command: str):
        parts = command.split(' ')  # TODO: Not good
        self.root_cli(parts)

    class Config:
        arbitrary_types_allowed = True



from fastapi import APIRouter
from pydantic import BaseModel, Field


class API(BaseModel):
    apis: list[APIRouter] = Field(default_factory=[])

    def start(self, app: 'EzApp'):
        for api in self.apis:
            # TODO: dependencies ?
            app.fast_api.include_router(api)

    class Config:
        arbitrary_types_allowed = True

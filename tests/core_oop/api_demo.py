import uvicorn
from fastapi import HTTPException, APIRouter, Request, FastAPI
from pydantic import BaseModel, Field

import easy_pysy as ez
from easy_pysy import uuid
from easy_pysy.core_oop.app import EzApp, current_app
from easy_pysy.core_oop.component import Singleton


class Message(BaseModel):
    id: str = Field(default_factory=uuid)
    content: str


class MessageRepository(Singleton):
    messages: dict[str, Message] = Field(default_factory=dict)

    def get(self, uuid: str):
        return self.messages[uuid]

    def contains(self, uuid: str):
        return uuid in self.messages

    def save(self, message: Message):
        self.messages[message.id] = message


app = EzApp(components=[MessageRepository])
api = FastAPI(lifespan=app.fast_api_lifespan)


@api.get('/messages/{uuid}')
def get_message(uuid: str) -> Message:
    repository = app.container.get(MessageRepository)

    ez.require(repository.contains(uuid), exception=HTTPException(status_code=404, detail="Foo not found"))
    return repository.get(uuid)


@api.post('/messages')
def save(message: Message) -> Message:
    repository = app.container.get(MessageRepository)

    repository.save(message)
    return message


if __name__ == '__main__':
    uvicorn.run(api, host='0.0.0.0', port=5000)


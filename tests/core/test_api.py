from fastapi import HTTPException, FastAPI
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

from easy_pysy import uuid, EzApp, Singleton, require


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

    require(repository.contains(uuid), exception=HTTPException(status_code=404, detail="Foo not found"))
    return repository.get(uuid)


@api.post('/messages')
def save(message: Message) -> Message:
    repository = app.container.get(MessageRepository)

    repository.save(message)
    return message


def test_get_and_post():
    with TestClient(api) as client:
        response = client.get('/messages/42')
        assert response.status_code == 404

        response = client.post('/messages', json={"content": "Hello"})
        assert response.status_code == 200
        created = response.json()

        response = client.get(f'/messages/{created["id"]}')
        assert response.status_code == 200
        assert response.json() == {"id": created["id"], "content": "Hello"}

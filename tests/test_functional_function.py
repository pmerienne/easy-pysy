import easy_pysi as ez


class User:
    def __init__(self, name: str):
        self.name = name


def say(self: User, message: str) -> str:
    return f"{message} from {self.name}"


def test_bind():
    user = User("Pierre")
    ez.bind(user, say)
    assert user.say("Hello") == "Hello from Pierre"


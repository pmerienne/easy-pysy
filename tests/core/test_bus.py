from pydantic import Field

from easy_pysy import EzApp, Service, Event, EventBus, on
from easy_pysy.core.component import Inject


class PingEvent(Event):
    message: str


class PongEvent(Event):
    message: str


class Player1(Service):
    bus: EventBus = Inject()
    received: list[PongEvent] = Field(default_factory=list)

    def play(self):
        self.bus.emit(PingEvent(message='Ping from player 1'))

    @on(PongEvent)
    def on_pong(self, pong: PongEvent):
        self.received.append(pong)


class Player2(Service):
    bus: EventBus = Inject()
    received: list[PingEvent] = Field(default_factory=list)

    def play(self):
        self.bus.emit(PongEvent(message='Pong from player 2'))

    @on(PingEvent)
    def on_pong(self, ping: PingEvent):
        self.received.append(ping)


def test_ping_pong():
    app = EzApp(components=[Player1, Player2])
    app.start()

    player_1 = app.container.get(Player1)
    player_2 = app.container.get(Player2)
    assert player_1.received == player_2.received == []

    player_1.play()
    assert len(player_2.received) == 1
    assert player_2.received[0].message == 'Ping from player 1'

    player_2.play()
    assert len(player_1.received) == 1
    assert player_1.received[0].message == 'Pong from player 2'


def test_call_decorated_method():
    app = EzApp(components=[Player1, Player2])
    app.start()

    player_1 = app.container.get(Player1)
    player_1.on_pong(PongEvent(message='PONG'))

    assert len(player_1.received) == 1
    assert player_1.received[0].message == 'PONG'



# TODO: log/store events
def test_store_events():
    # And it has been logged
    # events = ez.event.find_by_type(PingEvent)
    # assert events == [PingEvent(message='Hello')]
    pass


# TODO: app lifecycle event
import easy_pysi as ez
from easy_pysi import require
from tests.woofer import Woofer


class BarWoofer(Woofer):
    _created = False

    def __init__(self):
        # Ensure no singleton !
        require(BarWoofer._created is False, "Only 1 BarWoofer can exists")
        BarWoofer._created = True

    def say_woof(self) -> str:
        return 'Bar Woof'


@ez.provide(Woofer, singleton=True)
def create_woofer():
    return BarWoofer()

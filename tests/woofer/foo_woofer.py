import easy_pysi as ez
from tests.woofer import Woofer


class FooWoofer(Woofer):
    def say_woof(self) -> str:
        return 'Foo Woof'


@ez.provide(Woofer)
def create_woofer():
    return FooWoofer()

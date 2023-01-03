from multiprocessing.pool import ThreadPool

import easy_pysy as ez


class Woofer:
    def say_woof(self) -> str:
        raise RuntimeError('No woof !')


class BarWoofer(Woofer):
    _created = False

    def __init__(self):
        # Ensure no singleton !
        ez.require(BarWoofer._created is False, "Only 1 BarWoofer can exists")
        BarWoofer._created = True

    def say_woof(self) -> str:
        return 'Bar Woof'


@ez.provide(Woofer, singleton=True)
def create_bar_woofer():
    return BarWoofer()


def test_provide_using_last_provider(ez_app):
    woofer = ez.get(Woofer)
    assert woofer.say_woof() == 'Bar Woof'
    assert woofer == ez.get(Woofer)  # Singleton


def test_thread_safe_singleton_provider(ez_app):
    nb_threads = 100
    pool = ThreadPool(nb_threads)
    woofers = pool.map(lambda _: ez.get(Woofer), range(nb_threads))

    for woofer in woofers:
        assert woofer == woofers[0]

from multiprocessing.pool import ThreadPool

import easy_pysy as ez


class TheOnlyOne(ez.Singleton):
    pass


class NotASingleton:
    pass


def test_singleton_are_unique():
    assert NotASingleton() != NotASingleton()
    assert TheOnlyOne() == TheOnlyOne()


def test_thread_safe_singleton():
    nb_threads = 100
    pool = ThreadPool(nb_threads)
    singletons = pool.map(lambda _: TheOnlyOne(), range(nb_threads))
    assert all(singleton == singletons[0] for singleton in singletons)


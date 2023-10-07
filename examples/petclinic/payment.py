from typing import ClassVar

from easy_pysy import Service


class PaymentPlatform(Service):
    def pay(self, amount: float):
        raise NotImplementedError()


class CBPaymentPlatform(PaymentPlatform):
    profile: ClassVar[str] = 'prod'

    def pay(self, amount: float):
        if amount > 300:
            raise RuntimeError('Card declined')


class TestPaymentPlatform(PaymentPlatform):
    profile: ClassVar[str] = 'test'

    def pay(self, amount: float):
        pass

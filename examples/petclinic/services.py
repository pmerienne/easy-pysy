from datetime import datetime
from random import randint
from typing import Optional

from pydantic import Field

from easy_pysy import Service, uuid, on, AppStarted, EnvField, require, EventBus, loop
from easy_pysy.core.component import Inject
from examples.petclinic.model import Visit, Owner, VisitBooked, Pet, PetType, PetCreated
from examples.petclinic.payment import PaymentPlatform


class PetService(Service):
    bus: EventBus = Inject()
    repository: list[Pet] = Field(default_factory=list)

    def get_by_name(self, name: str) -> Optional[Pet]:
        for pet in self.repository:
            if name == pet.name:
                return pet
        return None

    def count(self) -> int:
        return len(self.repository)

    def find_all(self):
        return self.repository

    def create(self, name: str, pet_type: PetType, owner: Owner):
        pet = Pet(id=uuid(), name=name, type=pet_type, owner_id=owner.id)
        self.repository.append(pet)
        self.bus.emit(PetCreated(pet=pet))
        return pet

    def get_by_id(self, pet_id: str) -> Optional[Pet]:
        for pet in self.repository:
            if pet_id == pet.id:
                return pet
        return None

    def save(self, pet: Pet):
        self.delete(pet.id)
        self.repository.append(pet)

    def delete(self, pet_id: str):
        self.repository = [
            pet for pet in self.repository
            if pet.id != pet_id
        ]


class VisitService(Service):
    bus: EventBus = Inject()
    payment: PaymentPlatform = Inject()
    pets: PetService = Inject()
    repository: list[Visit] = Field(default_factory=list)
    visit_price: float = EnvField(default=42)

    def find_all(self) -> list[Visit]:
        return self.repository

    def count(self) -> int:
        return len(self.repository)

    def book(self, name: str, at: datetime):
        pet = self.pets.get_by_name(name)
        require(pet is not None, f"No pet found with name: {name}")

        self.payment.pay(self.visit_price)

        visit = Visit(id=uuid(), pet=pet, price=self.visit_price, at=at)
        self.repository.append(visit)
        self.bus.emit(VisitBooked(visit=visit))
        return visit

    def find_by_pet_id(self, pet_id: str) -> list[Visit]:
        return [
            visit
            for visit in self.repository
            if visit.pet.id == pet_id
        ]

    @loop(every_ms=500)
    def auto_book_to_make_money(self):
        all_pets = self.pets.find_all()
        for pet in all_pets:
            self.book(pet.name, datetime.now())


class OwnerService(Service):
    repository: list[Owner] = Field(default_factory=list)
    pets: PetService = Inject()

    def find_all(self) -> list[Owner]:
        return self.repository

    def count(self) -> int:
        return len(self.repository)

    def create(self, name: str, address: str) -> Owner:
        owner = Owner(id=uuid(), name=name, address=address)
        self.repository.append(owner)
        return owner

    @on(AppStarted)
    def init_data(self, event: AppStarted):
        owner = self.create('Dr. Evil’s', 'Unknown Lair')
        self.pets.create(name=f'Cat #{randint(0, 100)}', pet_type=PetType.CAT, owner=owner)


class StatsService(Service):
    pet_service: PetService = Inject()
    visit_service: VisitService = Inject()
    owner_service: OwnerService = Inject()

    def get_stats(self):
        return {
            "nb_pets": self.pet_service.count(),
            "nb_visits": self.visit_service.count(),
            "nb_owners": self.owner_service.count(),
        }


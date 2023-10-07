from typing import Any

from pydantic import Field

from easy_pysy import inject, require
from easy_pysy.core.component import Inject
from easy_pysy.plugins.ui.page import Page
from easy_pysy.plugins.ui.reactivity import js, JSMethod
from easy_pysy.plugins.ui.state import RouterState
from examples.petclinic.model import Pet, Visit, Owner, PetType
from examples.petclinic.services import PetService, StatsService, VisitService, OwnerService


class Home(Page):
    nb_pets: int
    nb_owners: int
    nb_visits: int

    @classmethod
    def fetch_state(cls, router_state: RouterState):
        stats_service = inject(StatsService)
        return stats_service.get_stats()

    def see_pet(self, pet_id: str):
        self.context.router.navigate(f'/pets/{pet_id}')


class Pets(Page):
    pet_service: PetService = Inject()
    owner_service: OwnerService = Inject()

    pets: list[Pet] = Field(default_factory=list)

    new_pet_name: str = ''
    new_pet_type: PetType = PetType.CAT

    close_modal = JSMethod("console.log('Closing !', this)")

    @classmethod
    def fetch_state(cls, router_state: RouterState):
        pet_service = inject(PetService)
        return {"pets": pet_service.find_all()}

    def see_pet(self, pet_id: str):
        self.context.router.navigate(f'/pets/{pet_id}')

    def create_pet(self):
        owner = self.owner_service.find_all()[0]  # TODO: ???
        pet = self.pet_service.create(self.new_pet_name, self.new_pet_type, owner)
        self.close_modal()  # TODO: execute now ! + async ==> NEED A WS
        # self.context.router.navigate(f'/pets/{pet.id}')


class Visits(Page):
    visits: list[Visit] = Field(default_factory=list)

    @classmethod
    def fetch_state(cls, router_state: RouterState):
        visit_service = inject(VisitService)
        return {"visits": visit_service.find_all()[:5]}

    def see_visit(self, visit_id: str):
        self.context.router.navigate(f'/visits/{visit_id}')


class Owners(Page):
    owners: list[Owner] = Field(default_factory=list)

    @classmethod
    def fetch_state(cls, router_state: RouterState):
        owner_service = inject(OwnerService)
        return {"owners": owner_service.find_all()}

    def see_owner(self, owner_id: str):
        self.context.router.navigate(f'/owners/{owner_id}')


class EditPet(Page):
    pet_service: PetService = Inject()
    pet_id: str
    pet: Pet

    @classmethod
    def fetch_state(cls, router_state: RouterState) -> dict[str, Any]:
        pet_service = inject(PetService)
        pet_id = router_state.params['pet_id']
        pet = pet_service.get_by_id(pet_id)
        require(pet is not None, f"No pet found for id {pet_id}")
        return {"pet_id": pet_id, "pet": pet}

    def save(self):
        self.pet_service.save(self.pet)

    def cancel(self):
        self.pet = self.pet_service.get_by_id(self.pet_id)

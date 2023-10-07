from fastapi import APIRouter

import easy_pysy as ez
from examples.petclinic.services import VisitService, OwnerService

crud_api = APIRouter(prefix='/crud')


@crud_api.get("/visits")
async def get_visits():
    visits = ez.get(VisitService)
    return visits.find_all()


@crud_api.get("/owners")
async def get_owners():
    owners = ez.get(OwnerService)
    return owners.find_all()

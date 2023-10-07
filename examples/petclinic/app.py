from easy_pysy import EzApp
from easy_pysy.plugins.api import API
from easy_pysy.plugins.cli import CLI
from easy_pysy.plugins.ui.plugin import UI
from examples.petclinic.api.crud import crud_api
from examples.petclinic.cli.crud import crud_cli
from examples.petclinic.cli.server import server_cli
from examples.petclinic.payment import CBPaymentPlatform, TestPaymentPlatform
from examples.petclinic.services import VisitService, OwnerService, PetService, StatsService
from examples.petclinic.ui.elements import HelloWorld, NavBar
from examples.petclinic.ui.pages import Home, EditPet, Pets, Visits, Owners

app = EzApp(
    # TODO: auto import components, pages, ...
    profile='prod',
    components=[VisitService, OwnerService, PetService, CBPaymentPlatform, TestPaymentPlatform, StatsService],
    api=API(
        apis=[crud_api]
    ),
    ui=UI(
        elements=[HelloWorld, NavBar],
        pages={
            "/": Home,
            "/pets": Pets, "/pets/{pet_id}": EditPet,
            "/visits": Visits,  # "/visits/{visit_id}": EditPet,
            "/owners": Owners,  # "/owners/{owner_id}": EditPet,
        },
        style_sheets=[
            # 'https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css',
            'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
            'https://cdn.jsdelivr.net/npm/uikit@3.16.22/dist/css/uikit.min.css'
        ],
        scripts=[
            'https://cdn.jsdelivr.net/npm/uikit@3.16.22/dist/js/uikit.min.js',
        ]
    ),
    cli=CLI(clis=[server_cli, crud_cli]),
)

if __name__ == '__main__':
    # uvicorn.run('app:app.fast_api', host='0.0.0.0', port=5000, reload=True)
    # app.run('crud list-owners')
    app.run('server start --reload')

from lib.route import add_route
from app_server.main import main


def configure_routes(request):
    add_route('', main.index)




from lib.route import add_route
from app_server.main import main

app_params = {
    'debug' : True,
    'title': 'Minha Venda'
}

def configure_routes(request):
    add_route('', main.index)




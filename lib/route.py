from lib.response import ResponseHTML, ResponseError


routes = {
}

def add_route(url, method):
    routes.update({url : method})

def execute_route(url, request):
    method = None
    key = url
    if key[-1:] == '/':
        key = key[:-1]
    if key in routes:
        method = routes[key]
        return method(request)
    else:
        return None
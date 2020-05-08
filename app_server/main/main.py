from lib.response import ResponseHTML, ResponseError

def index(request) : 
    if request.command == 'GET':
        return ResponseHTML().response('app/main/index.html', request.params)
    else:
        return ResponseError().response(403, 'Method {method} not allowed'.format(method=request.command))

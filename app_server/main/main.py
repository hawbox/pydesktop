from lib.response import ResponseHTML, ResponseError
#from configure_app import app_params
def index(request) : 
    if request.command == 'GET':
        request.params.update({'title': request.application_params['title']})
        return ResponseHTML().response('app/main/index.html', request.params)
    else:
        return ResponseError().response(403, 'Method {method} not allowed'.format(method=request.command))

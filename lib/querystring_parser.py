from urllib.parse import parse_qs

def parse_query_string(query_string):
    params = parse_qs(query_string)
    new_params = {}
    
    for key in params:
        new_params.update({key: params[key][0]})

    return new_params
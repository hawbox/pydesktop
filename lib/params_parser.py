import os
import sys

from lib.multipart_form_data_parser import parse_multipart_form_data
from lib.querystring_parser import parse_query_string

CONTENT_TYPE_MULTIPART_FORM_DATA = 'multipart/form-data'
CONTENT_TUYPE_QUERY_STRING = 'querystring'

parse_methods = {
    CONTENT_TYPE_MULTIPART_FORM_DATA : parse_multipart_form_data,
    CONTENT_TUYPE_QUERY_STRING: parse_query_string
}



def parse_params(bytes_params, param_type):
    method = parse_methods[param_type]  
    if method:
        return method(bytes_params)
    else:
        Exception('The content type ' + param_type + ' is not suported')


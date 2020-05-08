import json
import os
import sys
from lib.config import PROJECT_ROOT
from lib.template_functions import replace_template_variables


class StantardResponse(object):
    def __init__(self):
        super().__init__()
        self.status = 200
        self.response_type = 'text/html'
        self.success = True
        self.response_text = ""
        self.error_message = ""
      
class ResponseError(StantardResponse):
    def __init__(self):
        super().__init__()
    
    def response(self, code, message):
        self.status = code
        self.success = False
        self.error_message = message
        return self


class ResponseHTML(StantardResponse):
    def __init__(self):
        super().__init__()
    
    def response(self, template_path, parameters = {}):
        try:
            with open(os.path.join(PROJECT_ROOT, template_path), 'r') as f:
                self.response_text = f.read()
            self.response_text = replace_template_variables(self.response_text, parameters)
            self.status = 200
            self.success = True
                 
        except FileNotFoundError as e:             
            self.status = 404
            self.success = False
            self.error_message = "Template {template} not found".format(template=template_path) 
        except Exception as e: 
            self.status = 500
            self.success = False
            self.error_message = str(e)
        
        return self
    
    def simple_response(self, html):
        self.response_text = html
        self.status = 200
        self.success = True

        return self

class ResponseJson(StantardResponse):
    def __init__(self):
        super().__init__()
        self.response_type = 'application/json'

    def response(self, json_object):
        try:
            self.response_text = json.dumps(json_object)
        except Exception as e: 
            self.status = 500
            self.success = False
            self.error_message = str(e)
     
        return self

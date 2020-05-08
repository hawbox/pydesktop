import os
import sys
from lib.crawler import execute_regex
from lib.config import PROJECT_ROOT

def include_templates(text):
    templates = execute_regex('\[\{ *include_template *\((.*?)\) *\}\]', text)
    for template in templates:
        completo = execute_regex('\[\{ *include_template *\(' + template + '\) *\}\]', text)
        if len(completo) > 0:
            completo = completo[0]
        if completo:
            try:
                with open(PROJECT_ROOT + template, 'r') as template_file:
                    text_file = template_file.read()
                text = text.replace(completo, text_file)
            except FileNotFoundError as e:
                raise Exception(str(e))
            except Exception as e:
                raise
        
    return text

def replace_template_variables(text, dictionary):
    text = include_templates(text)
    for key in dictionary:
        text = text.replace('[{' + key +'}]', dictionary[key])
    return text
from lib.crawler import execute_regex

def parse_multipart_form_data(byte_params):
    params_list = byte_params.decode('utf-8').split('\r\n')
    step_next = False
    key = ""
    values = {}
    for line in params_list:
        if step_next:
            step_next = False
            continue

        if 'Content-Disposition: form-data' in line:
            step_next = True
            key = execute_regex('name="(.*?)"', line, True)[0]
        elif key:
            values.update({key: line})
            key = None            

    return values


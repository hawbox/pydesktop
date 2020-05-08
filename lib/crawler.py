from urllib import request
import re
import ssl


def execute_regex(expression, text, empty_str_if_not_found = False, group_index = None):
    result = []
    got = re.findall(expression, text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    for item in got:
        if type(item) == tuple:
            if group_index != None:
                result.append(item[group_index])
            else:
                a = ""
                for x in item:
                    a += x
                result.append(a)
        else:
            result.append(item)

    if empty_str_if_not_found:
       if len(result) == 0:
            return [""]
    return result

class PageReader(object):
    def __init__(self, link, list_regex_to_links,  list_regex_to_text):
        self.__step_find_link = list_regex_to_links        
        self.__step_find_text = list_regex_to_text
        self.__link = link

    def get_page_html(self, link, encode_inf):
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        with request.urlopen(url=link, context=gcontext) as f:
            text = f.read().decode(encode_inf)
        return text
        

    def __execute_regex(self, list_text, regex):
        result = []
        for text in list_text:
            result += execute_regex(regex, text)
        return result

    def get_links(self):
        html = self.get_page_html(self.__link, 'utf-8')
        if self.__step_find_link:
            result = [html]
            for regex in self.__step_find_link:
                result = self.__execute_regex(result, regex)
            return result
        return [self.__link]

    def get_data(self):
        html = ""
        data = []
        result = []
        links = self.get_links()

        for link in links:
            html = self.get_page_html(link, 'utf-8')
            data = [html]

            for regex in self.__step_find_text:
                data = self.__execute_regex(data, regex)

            for d in data:
                result.append({"link": link,  "data":d})
        return result
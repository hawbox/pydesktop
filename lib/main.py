import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json

from lib import route
from lib.crawler import execute_regex

from lib.params_parser import parse_params

host = '127.0.0.1'
port = 8083
server_address = (host, port)
base_url = 'http://' + host + ':' + str(port)

try:
    import msvcrt
    has_msvcrt = True
except:
    has_msvcrt = False


class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    route_configurator_method = None
    def __init__(self, *args, directory=None, **kwargs):        
        if self.route_configurator_method:
            self.route_configurator_method()
        super().__init__(*args, **kwargs)
        

    def get_MIME(self, key):
        mime = {
                ".aac": "audio/aac",
                ".abw": "application/x-abiword",
                ".arc": "application/octet-stream",
                ".avi": "video/x-msvideo",
                ".azw": "application/vnd.amazon.ebook",
                ".bin": "application/octet-stream",
                ".bz": "application/x-bzip",
                ".bz2": "application/x-bzip2",
                ".csh": "application/x-csh",
                ".css": "text/css",
                ".csv": "text/csv",
                ".doc": "application/msword",
                ".eot": "application/vnd.ms-fontobject",
                ".epub": "application/epub+zip",
                ".gif": "image/gif",
                ".htm": "",
                ".html": "text/html",
                ".ico": "image/x-icon",
                ".ics": "text/calendar",
                ".jar": "application/java-archive",
                ".jpeg": "",
                ".jpg": "image/jpeg",
                ".js": "application/javascript",
                ".json": "application/json",
                ".mid": "",
                ".midi": "audio/midi",
                ".mpeg": "video/mpeg",
                ".mpkg": "application/vnd.apple.installer+xml",
                ".odp": "application/vnd.oasis.opendocument.presentation",
                ".ods": "application/vnd.oasis.opendocument.spreadsheet",
                ".odt": "application/vnd.oasis.opendocument.text",
                ".oga": "audio/ogg",
                ".ogv": "video/ogg",
                ".ogx": "application/ogg",
                ".otf": "font/otf",
                ".png": "image/png",
                ".pdf": "application/pdf",
                ".ppt": "application/vnd.ms-powerpoint",
                ".rar": "application/x-rar-compressed",
                ".rtf": "application/rtf",
                ".sh": "application/x-sh",
                ".svg": "image/svg+xml",
                ".swf": "application/x-shockwave-flash",
                ".tar": "application/x-tar",
                ".tif": "",
                ".tiff": "image/tiff",
                ".ts": "application/typescript",
                ".ttf": "font/ttf",
                ".vsd": "application/vnd.visio",
                ".wav": "audio/x-wav",
                ".weba": "audio/webm",
                ".webm": "video/webm",
                ".webp": "image/webp",
                ".woff": "font/woff",
                ".woff2": "font/woff2",
                ".xhtml": "application/xhtml+xml",
                ".xls": "",
                ".xlsx": "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "",
                ".xml": "application/xml",
                ".xul": "application/vnd.mozilla.xul+xml",
                ".zip": "application/zip",
                ".3gp": "video/3gpp",
                "audio/3gpp": "",
                ".3g2": "video/3gpp2",
                "audio/3gpp2": "",
                ".7z": "application/x-7z-compressed",
                ".map" : "magnus-internal/imagemap"
                }
                
        if not key in mime:
            result =  'text/html'
        else:
            result = mime[key]
        
        return result
    
    def do_OPTIONS(self):           
        self.send_response(200)       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header("Access-Control-Allow-Headers", '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.end_headers()
        
        return
    
    def do_GET(self):
        path = '' if self.path == '/' else self.path[1:]
        path_splited =  path.split('?')                  
        path = path_splited[0]
                        
        sendReply = False
        extension = os.path.splitext(path)[1].lower()
        mimetype = self.get_MIME(extension)
    
        sendReply = len(mimetype) > 0
        
        if sendReply == True:
            # Send headers
            #self.data_string = self.rfile.read(int(self.headers['Content-Length']))

            try:                
                self.params = []
                if len(path_splited) > 1:
                    self.params = parse_params(path_splited[1], 'querystring')

                result = route.execute_route(path, self)                
                if result:
                    self.send_response(result.status)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header("Access-Control-Allow-Headers", '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                    self.send_header('Content-type', result.response_type)
                    self.end_headers()   
                    if result.success:
                        self.wfile.write(bytes(result.response_text, encoding='utf8'))
                        return 
                    else:
                        self.send_error(result.status, result.error_message)       
                else:
                    with open(path, 'rb') as f: 
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header("Access-Control-Allow-Headers", '*')
                        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                        self.send_header('Content-type', mimetype)
                        self.end_headers() 
                        self.wfile.write(bytes(f.read()))
                        

                    return
            except IOError:
                self.send_error(404, 'File Not Found: %s' % path)
            except Exception as e:
                self.send_error(500, str(e))   
        return 

    def do_POST(self):
        path = '' if self.path == '/' else self.path[1:]
        path_splited =  path.split('?')                  
        path = path_splited[0]
                 
        if len(path_splited) > 1:
            self.send_error(403, 'Query params not permited for post')
        
        sendReply = False
        mimetype = self.get_MIME(os.path.splitext(path)[1])
    
        sendReply = len(mimetype) > 0
        
        if sendReply == True:
            # Send headers
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            self.params = parse_params(self.data_string, self.headers.get_content_type())

            try:
                result = route.execute_route(path, self)
                if result:
                    self.send_response(result.status)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header("Access-Control-Allow-Headers", '*')
                    self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                    self.send_header('Content-type', result.response_type)
                    self.end_headers()   
                    if result.success:
                        self.wfile.write(bytes(result.response_text, encoding='utf8'))
                        return 
                    else:
                        self.send_error(result.status, result.error_message)       
                else:
                    self.send_error(500, str(e))       
            except IOError:
                self.send_error(404, 'File Not Found: %s' % path)
            except Exception as e:
                self.send_error(500, str(e))   
        return

def kbfunc():
    if not has_msvcrt:
        return 0

    x = msvcrt.kbhit()
    if x:
       ret = ord(msvcrt.getch())
    else:
       ret = 0
    return ret

def chek_key_press(server_class):    
    if not has_msvcrt:
        return

    while True:
        try:
            time.sleep(1)
            x = kbfunc()            
            if x == 4: # Ctrl-D            
                raise KeyboardInterrupt('Execution interrupted by user.')            
        except KeyboardInterrupt as identifier:                                    
            server_class.shutdown()
            server_class.socket.close()            
            #server_th
            #server_sd_th, 
            #check_fl_th            
            break


class HTTPServerBreak(HTTPServer):
    def service_actions(self):        
        x = kbfunc()                    
        if x == 4: # Ctrl-D            
            raise KeyboardInterrupt('Execution interrupted by user.')        

def serve(route_configurator, debugging = False):    
    print('starting server...')
    testHTTPServer_RequestHandler.route_configurator_method = route_configurator
    httpd = HTTPServerBreak(server_address, testHTTPServer_RequestHandler)
    print('running server at ' + base_url + '...')
    print('To stop, press CTRL + D on windows or CTRL + C on UNIX based systems')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    #  server_address = ('127.0.0.1', 8081)
    #th_check_press = threading.Thread(target=chek_key_press, args=(httpd,))
    #th_check_press.start()
    httpd.serve_forever()
     
    raise Exception('Server closed by user.')

#serve()
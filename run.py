import threading
import webview
from lib.main import get_server, base_url
from configure_app import configure_routes, app_params

if __name__ == '__main__':
    
    window = webview.create_window(title=app_params['title'], url=base_url)
    server = get_server(configure_routes, app_params)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
       
    window.closing += lambda : server.shutdown()
    window.closing += lambda : window.destroy()
    webview.start(debug=app_params['debug'])


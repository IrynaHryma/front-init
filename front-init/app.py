import json
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes

import threading


from jinja2 import Environment, FileSystemLoader

BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

env = Environment(loader=FileSystemLoader("templates"))



class HTTPHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        body = urllib.parse.unquote_plus(body.decode())
        payload = {key:value for key, value in[ el.split("=") for el in body.split("&")]}
        
        data_fila = DATA_DIR/"data.json"
        with data_fila.open("a", encoding="utf-8") as fd:
            json.dump(payload,fd, ensure_ascii=False)
            fd.write("\n")
        
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()



    def do_GET(self):
        route = urllib.parse.urlparse(self.path).path
        match route:
            case "/":
                self.send_html("index.html")

            case "/message":
                self.send_html("message.html")

            case _:
                
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:   
                    self.send_html("error.html", 404)

    
    def send_html(self, html_content, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))
    
            
    def render_template(self, template_name, context=None):
        if context is None:
            context={}

        template = env.get_template(template_name)
        html_content = template.render(context)
        return html_content   


    def send_static(self,file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
                
            self.send_error("error.html", 404)


def run(server=HTTPServer, handler=HTTPHandler):
    address = ("", 3000)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

def start_client():
    import client
    client.main()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run)
    server_thread.start()

    client_thread = threading.Thread(target=start_client)
    client_thread.start()
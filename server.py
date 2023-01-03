import http.server
import socketserver
import json
import data

data = data.users


class FakeAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/users':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Not Found'.encode())


PORT = 8000

with socketserver.TCPServer(("", PORT), FakeAPIHandler) as httpd:
    print(f'Serving at port {PORT}...')
    httpd.serve_forever()


def do_POST(self):
    if self.path == '/users':
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        new_user = json.loads(body)
        data.append(new_user)
        self.send_response(201)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Created'.encode())
    else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Not Found'.encode())


def do_PUT(self):
    if self.path.startswith('/users'):
        user_id = int(self.path.split('/')[-1])
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        updated_user = json.loads(body)
        for user in data:
            if user['id'] == user_id:
                user['name'] = updated_user['name']
                break
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Updated'.encode())
    else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Not Found'.encode())


def do_DELETE(self):
    if self.path.startswith('/users/'):
        user_id = int(self.path.split('/')[-1])
        for user in data:
            if user['id'] == user_id:
                data.remove(user)
                break
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Deleted'.encode())
    else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Not Found'.encode())

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import json
import os
from manager_request_implementer import ManagerRequestImplementer

class ManagerServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, handler):
        HTTPServer.__init__(self, address, handler)


class ManagerRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.path)
        mri = ManagerRequestImplementer()
        if self.path == "/cover_shifts":
            time = self.headers.getheader('time')
            message = mri.cover_shifts(time)
            print(message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
        elif self.path == "/switch_shifts":
            old_time = self.headers.getheader('old_time')
            new_time = self.headers.getheader('new_time')
            from_person = self.headers.getheader('from_person')
            to_person = self.headers.getheader('to_person')
            message = mri.swap_shifts(old_time, new_time, from_person, to_person)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
        else:
            self.send_response(404)

PORT = 10000

Handler = ManagerRequestHandler

httpd = ManagerServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

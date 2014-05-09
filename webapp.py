#!/usr/bin/env python
'''
Start a Hello World server.
'''
from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return ('Hello, World.',)

def start():
    httpd = make_server('localhost', 8000, application)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        raise SystemExit(0)

if __name__ == '__main__':
    start()

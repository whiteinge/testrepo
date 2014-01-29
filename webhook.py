#!/usr/bin/env python
'''
An app to fire Salt events based on data from Travis-CI builds

'''
import json

from wsgiref.simple_server import make_server

import salt.client
import salt.exceptions

MYSECRET = '8H8#i*rsS)P1PUFomQAa'

def fire_salt_event(data):
    if not 'mysecret' in data or data['mysecret'] != MYSECRET:
        return False

    caller = salt.client.Caller()
    return caller.sminion.functions['event.fire_master'](
            data=json.dumps(data),
            tag='myapp/build/suceeded')

def process_request(environ):
    method = environ['REQUEST_METHOD'].upper()

    if method == 'GET':
        code = '406 NOT ACCEPTABLE'
        resp = 'Only POST requests are accepted.'
        return code, resp
    elif method == 'POST':
        content_type = environ.get('CONTENT_TYPE', '')

        if content_type != 'application/json':
            code = '406 NOT ACCEPTABLE'
            resp = 'Content-type not supported.'
            return code, resp

        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)
        body = environ['wsgi.input'].read(length)

        try:
            data = json.loads(body)
        except ValueError as exc:
            code = '400 BAD REQUEST'
            resp = 'Error parsing JSON: {0}'.format(exc)
            return code, resp
        else:
            try:
                event_fired = fire_salt_event(data)
            except salt.exceptions.SaltException as exc:
                code = '500 INTERNAL SERVER ERROR'
                resp = 'An unknown error occurred: {0}'.format(exc)
            else:
                if not event_fired:
                    code = '401 UNAUTHORIZED'
                else:
                    code = '200 OK'
                resp = json.dumps({'success': event_fired, 'data': data})

    else:
        code = '405 METHOD NOT ALLOWED'
        resp = 'Method not allowed.'

    return code, resp

def application(environ, start_response):
    code, resp = process_request(environ)

    start_response(code, [('Content-Type', 'application/json')])
    return (resp,)

def start():
    httpd = make_server('localhost', 8001, application)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        raise SystemExit(0)

if __name__ == '__main__':
    start()

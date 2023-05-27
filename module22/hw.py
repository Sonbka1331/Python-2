import json


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    path = environ['PATH_INFO']

    if path == '/hello':
        response = {'message': 'Hello, world!'}
    elif path.startswith('/hello/'):
        username = path.split('/')[-1]
        response = {'message': f'Hello, {username}!'}
    else:
        status = '404 Not Found'
        response = {'error': 'Page not found'}

    response_body = json.dumps(response).encode('utf-8')

    start_response(status, headers)

    return [response_body]

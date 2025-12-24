import os


def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    
    if path == '/static':
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'static', 'test_file.txt')
            with open(file_path, 'rb') as f:
                response_body = f.read()
            status = '200 OK'
        except FileNotFoundError:
            status = '404 Not Found'
            response_body = b'Not Found'
            
    elif path == '/dynamic':
        response_body = b'A' * 102400
        status = '200 OK'
        
    else:
        status = '404 Not Found'
        response_body = b'Not Found'

    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]

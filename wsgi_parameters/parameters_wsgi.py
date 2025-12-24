from urllib.parse import parse_qs


def application(environ, start_response):
    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)

    request_body_size = int(environ.get('CONTENT_LENGTH', 0))

    request_body = environ['wsgi.input'].read(request_body_size)
    post_params = parse_qs(request_body.decode('utf-8'))

    output = []
    output.append(b"GET Parameters:\n")
    if get_params:
        for key, values in get_params.items():
            for value in values:
                output.append(f"  {key}: {value}\n".encode('utf-8'))
    else:
        output.append(b"  None\n")

    output.append(b"\nPOST Parameters:\n")
    if post_params:
        for key, values in post_params.items():
            for value in values:
                output.append(f"  {key}: {value}\n".encode('utf-8'))
    else:
        output.append(b"  None\n")

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, response_headers)
    return output

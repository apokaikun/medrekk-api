from fastapi import Request


def get_host(
        request: Request,
) -> str : 
    return request.headers.get('host')
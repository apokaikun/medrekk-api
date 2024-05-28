from fastapi import status

from .main import login

def test_auth():
    token = login()
    assert token != None

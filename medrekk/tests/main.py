from fastapi import status
from fastapi.testclient import TestClient
from medrekk.main import medrekk_app
from medrekk.common.utils.shortid import shortid

client = TestClient(app=medrekk_app, base_url="http://medrekk.com:8000")

def login() -> str | None:
    response = client.post(
        url="/auth",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "test@a.com", "password": "aaaa"},
    )

    if response.status_code == status.HTTP_200_OK:
        response_body = response.json()
        token = response_body['access_token']
        return token

    return None

class TestNewAccount:
    def __init__(self, client: TestClient, root_path: str) -> None:
        self.client = client
        self.name = shortid()
        self.account_name = f'fast {self.name}'
        self.user_name = f'{self.name}@a.com'
        self.password = 'aaaa'
        self.root_path = root_path or ''
        self.account = None
        self.token = None

    @property
    def data(self):
        return {
        "account_name": self.account_name,
        "user_name": self.user_name,
        "password": self.password,
    }

    @property
    def sub_domain(self):
        return '-'.join(self.account_name.lower().split())
    
    def login(self):
        response = self.client.post(
            url='/auth',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'username': self.user_name,
                'password': self.password
            }
        )
        if response.status_code == status.HTTP_200_OK:
            self.token = response.json()['access_token']


test_new_account = TestNewAccount(client=client, root_path=medrekk_app.root_path)

__all__ = [
    'test_new_account',
]
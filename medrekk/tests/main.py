from fastapi.testclient import TestClient
from medrekk.main import medrekk_app
from medrekk.common.utils.shortid import shortid

client = TestClient(app=medrekk_app, base_url="http://medrekk.com:8000")

class TestAccount:
    def __init__(self, client: TestClient, root_path: str) -> None:
        self.client = client
        self.name = shortid()
        self.account_name = f'fast {self.name}'
        self.user_name = f'{self.name}@a.com'
        self.password = 'aaaa'
        self.root_path = root_path or ''

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

test_account = TestAccount(client=client, root_path=medrekk_app.root_path)

__all__ = [
    'test_account',
]
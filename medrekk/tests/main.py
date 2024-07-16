from typing import Optional

from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from medrekk.common.utils.shortid import shortid
from medrekk.main import medrekk_app

client = TestClient(app=medrekk_app, base_url="http://medrekk.com:8000")

def clientmaker(app: FastAPI, base_url: str):
    return TestClient(app=app, base_url=base_url)


client_admin = clientmaker(app=medrekk_app, base_url="http://medrekk.com:8000")


def login(username: str, password: str, client: TestClient) -> dict | None:
    response = client.post(
        url="/auth",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )

    if response.status_code == status.HTTP_200_OK:
        response_body = response.json()
        return response_body
    print(username, password, response.status_code)
    return None


class TestAccount:
    def __init__(
        self, root_path: str, account_name: Optional[str] = None, client: TestClient = None,
    ) -> None:
        self._client = client
        self.account_name = (
            f"fast {account_name}" if account_name else "awesome account"
        )
        self.username = f"{account_name}@a.com" if account_name else "test@a.com"
        self.password = "aaaa"
        self.root_path = root_path or ""
        self.account = None
        self.token = None

    @property
    def data(self):
        return {
            "account_name": self.account_name,
            "user_name": self.username,
            "password": self.password,
        }

    @property
    def sub_domain(self):
        return "-".join(self.account_name.lower().split())
    
    @property
    def client(self):
        if self._client:
            return self._client
        return clientmaker(app=medrekk_app, base_url="http://awesome-account.medrekk.com:8000")

    def login(self):
        response = self.client.post(
            url="/auth",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"username": self.username, "password": self.password},
        )

        if response.status_code == status.HTTP_200_OK:
            self.token = response.json()["access_token"]

    def logout(self):
        client.post(
            url=self.root_path + "/logout",
            headers={"Authorization": f"Bearer {self.token}"},
        )


test_new_account = TestAccount(
    client=client,
    account_name=shortid(),
    root_path=medrekk_app.root_path,
)

test_account_admin = TestAccount(
    client=client_admin,
    root_path=medrekk_app.root_path,
)

test_account = TestAccount(
    client=client,
    root_path=medrekk_app.root_path,
)

__all__ = [
    "test_account",
    "test_new_account",
]

from fastapi import status

from medrekk.tests.main import client, login, test_account, client_admin

username = "test@a.com"
password = "aaaa"


def test_auth():
    response = login(username=username, password=password, client=client_admin)

    assert response["access_token"] != None
    assert response["token_type"] == "bearer"


def test_logout():
    response = login(username=username, password=password, client=client_admin)
    token = response["access_token"]
    root_path = test_account.root_path
    logout_path = "/logout"
    response = client.post(
        url=root_path + logout_path, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == None

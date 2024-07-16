from fastapi import status

from medrekk.common.utils import routes, shortid
from medrekk.tests.main import client, test_account, login


def test_create_user():
    data = {"username": f"{shortid()}@a.com", "password": "aaaa"}
    test_account.login()
    url = test_account.root_path + f'/{routes.MEMBERS}'
    print(url)
    response = client.post(
        url=url,
        headers={"Authorization": f"Bearer {test_account.token}"},
        json=data,
    )
    new_user = response.json()
    print(new_user)
    assert response.status_code == status.HTTP_201_CREATED
    assert new_user["username"] == data["username"]
    assert new_user["active"] == True

    # Test login
    response = login(username=data['username'], password=data['password'])
    body = response.json()

    assert body['access_token'] != None
    assert body['token_type'] == 'bearer'

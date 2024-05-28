from medrekk.tests.main import login, test_new_account
from fastapi import status

client = test_new_account.client
root_path = test_new_account.root_path

def test_create_account():
    _account_path = '/accounts'
    data: dict = test_new_account.data
    response_account = client.post(
        root_path + _account_path,
        json=data,
    )

    body: dict = response_account.json()
    test_new_account.account = body

    assert body['account_name'] == test_new_account.account_name
    assert body['account_subdomain'] == test_new_account.sub_domain
    assert response_account.status_code == status.HTTP_201_CREATED

    test_new_account.login()

    assert test_new_account.token != None

def test_get_accounts():
    _account_path = '/accounts'

    token = login()

    response = client.get(
        url=root_path+ _account_path,
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    accounts = response.json()
    print(accounts)
    assert response.status_code == status.HTTP_200_OK
    assert accounts['id'] == '22ORdgJor4P'
    assert accounts['owner_id'] == '22ORdh3HZHK'
    assert accounts['account_name'] == 'awesome account'
    assert accounts['account_subdomain'] == 'awesome-account'
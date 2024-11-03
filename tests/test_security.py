from http import HTTPStatus

from jwt import decode

from fast_zero.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_jwt():
    data = {'sub': 'test'}
    token = create_access_token(data)
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_missing_token(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_jwt_missing_username(client, user):
    token = create_access_token(data={})
    response = client.put(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_none_user(client, user):
    token = create_access_token(data={'sub': 'test_none_user'})
    response = client.put(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_user_token_permission(client, token, user_second):
    response = client.delete(
        f'/users/{user_second.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_update = client.put(
        f'/users/{user_second.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user_second.username,
            'email': user_second.email,
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not permission'}
    assert response_update.status_code == HTTPStatus.FORBIDDEN
    assert response_update.json() == {'detail': 'Not permission'}

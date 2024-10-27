from datetime import datetime, timezone
from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_create_user(client):
    user_data = {
        'username': 'test',
        'email': 'test@example.com',
        'password': 'secret',
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@example.com',
        'created_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
    }


def test_create_user_username_conflict(client, user):
    user_data = {
        'username': 'test',
        'email': 'test@example.com',
        'password': 'secret',
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_conflict(client, user):
    user_data = {
        'username': 'test_one',
        'email': 'test@example.com',
        'password': 'secret',
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    user_schema['created_at'] = user_schema['created_at'].strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    user_schema['updated_at'] = user_schema['updated_at'].strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    user_schema['created_at'] = user_schema['created_at'].strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    user_schema['updated_at'] = user_schema['updated_at'].strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'user': user_schema}


def test_read_nonexistent_user(client):
    response = client.get('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    user_data = {
        'username': 'updated_test',
        'email': 'updated_test@example.com',
        'password': 'secret',
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'updated_test',
        'email': 'updated_test@example.com',
        'created_at': user.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
        'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
    }


def test_update_nonexistent_user(client):
    user_data = {
        'username': 'nonexistent_test',
        'email': 'nonexistent_test@example.com',
        'password': 'secret',
    }
    response = client.put('/users/100', json=user_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_username_conflict(client, user, user_second):
    user_data = {
        'username': 'test_second',
        'email': 'test_second@example.com',
        'password': 'secret',
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_update_user_email_conflict(client, user, user_second):
    user_data = {
        'username': 'updated_test',
        'email': 'test_second@example.com',
        'password': 'secret',
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_nonexistent_user(client):
    response = client.delete('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

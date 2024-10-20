from http import HTTPStatus


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
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'test', 'email': 'test@example.com'},
            # Add more users here if needed
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': {
            'id': 1,
            'username': 'test',
            'email': 'test@example.com',
        }
    }


def test_read_nonexistent_user(client):
    response = client.get('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_nonexistent_user(client):
    response = client.delete('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

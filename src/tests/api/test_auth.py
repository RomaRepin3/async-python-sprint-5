from http import HTTPStatus

from pytest import mark

from main import app


class TestAuth:

    @mark.anyio
    async def test_register(self, client, user_data):
        response = await client.post(app.url_path_for('register'), json=user_data)
        assert response.status_code == HTTPStatus.CREATED, response.text
        assert response.json() == {'status': True, 'message': 'The operation was successful'}, response.text

    @mark.anyio
    async def test_auth(self, client, user_data):
        response = await client.post(app.url_path_for('register'), json=user_data)
        assert response.status_code == HTTPStatus.CREATED, response.text
        assert response.json() == {'status': True, 'message': 'The operation was successful'}, response.text

        response = await client.post(
            '/api/auth',
            data={
                'username': user_data['login'],
                'password': user_data['password']
            }
        )
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json()['access_token'], response.text
        assert response.json()['token_type'] == 'bearer', response.text

    @mark.anyio
    async def test_auth_fail(self, client):
        response = await client.post(
            app.url_path_for('auth'),
            data={
                'username': 'test',
                'password': 'test'
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text

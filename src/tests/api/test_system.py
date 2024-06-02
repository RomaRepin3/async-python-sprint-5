from http import HTTPStatus

from main import app


class TestSystem:
    async def test_ping(self, client):
        response = await client.get(app.url_path_for('ping'))
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json()['db'] is not None, response.text
        assert response.json()['redis'] is not None, response.text
        assert response.json()['s3'] is not None, response.text

from http import HTTPStatus


def test_ping(client):
    response = client.get('/api/ping')
    assert response.status_code == HTTPStatus.OK, response.text
    assert response.json()['db'] is not None, response.text
    assert response.json()['redis'] is not None, response.text
    assert response.json()['s3'] is not None, response.text

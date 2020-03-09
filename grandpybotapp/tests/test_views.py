import views
import pytest
import urllib.request
from unittest.mock import Mock

def test_base_route(monkeypatch):
    client = views.app.test_client()
    url = '/'
    response = client.get(url)
    # def mockreturn(request, params):
    #     index = "Hello it's papy bot !"
    #     mock = Mock()
    #     mock.return_value = index
    #     return mock
    # monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)
    # assert response.get_data() == b"Hello it's papy bot !"
    assert response.status_code == 200

## Comment faire le test pour fonction location_request ???
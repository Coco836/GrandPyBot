import views
import pytest
import urllib.request
from unittest.mock import Mock, patch, MagicMock


def test_base_route():
    """Test index fonction."""
    client = views.app.test_client()
    url = '/'
    response = client.get(url)
    assert b"GrandPy Bot, ton papy robot" in response.get_data()
    assert response.status_code == 200


@patch.object(
            views.GoogleMapsApi, '__new__', Mock(return_value=Mock(
                address='mon adresse', longitude=12234, latitude=2134))
)
@patch.object(
            views.MediaWikiApi, '__new__', Mock(return_value=MagicMock(
                request_wiki_summary=Mock(return_value='toto')))
)
def test_location_request():
    """Test for location_request fonction"""
    client = views.app.test_client()
    url = '/'
    response = client.post(url, data={'user_input': 'Tour Eiffel'})
    assert response.status_code == 200

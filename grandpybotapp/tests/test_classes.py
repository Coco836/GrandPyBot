import classes
import pytest
import GrandPyBot.config as config
import urllib.request
from unittest.mock import Mock


class TestGrandPyBotConversation:
    """Test for GrandPyBotQuestions class."""

    def test_random_responses(self):
        """Test for random_response method."""
        test_random_response = classes.GrandPyBotConversation.random_response()
        assert test_random_response in classes.GrandPyBotConversation.responses

    def test_random_stories_introduction(self):
        """Test for random_story method."""
        test_random_story_intro = classes.GrandPyBotConversation.random_story()
        assert (
                test_random_story_intro
                in classes.GrandPyBotConversation.stories_intro
        )

    def test_random_end_stories_quote(self):
        """Test for random_end_quote method."""
        test_random_end_story_quote = (
                                        classes.GrandPyBotConversation.
                                        random_end_quote()
        )
        assert (
                test_random_end_story_quote
                in classes.GrandPyBotConversation.end_quotes
        )


class TestParser:
    """Test for Parser class."""

    def test_letter_case(self):
        """Test for arrange_input method."""
        test_phrase = (
                        classes.Parser.
                        arrange_input('Avenue Champs-Elysées Paris France')
        )
        assert test_phrase == 'avenue champs elysées paris france'

    def test_stopwords(self):
        """Test for arrange_input method."""
        test_quote = (
                        classes.Parser.arrange_input(
                                                    "Salut GrandPy,"
                                                    "Est-ce que tu connais "
                                                    "adresse d'OpenClassrooms?"
                                                    )
        )
        assert test_quote == "openclassrooms"


class TestGoogleMapsApi():
    """Test for GoogleMapsApi class."""

    def test_geocode(self, monkeypatch):
        """Test for get_address_geolocation method."""
        def mockreturn(request, key, method):
            address_details = {
                                'lat': 4.235, 'lng': 1.435436,
                                'address': "addresse de la tour eiffel"
            }
            return Mock(json=address_details)
        monkeypatch.setattr(classes.geocoder, 'google', mockreturn)
        assert (
            classes.GoogleMapsApi('tour eiffel').get_address_geolocation() ==
            (4.235, 1.435436, "addresse de la tour eiffel")
        )

    def test_try_block(self, monkeypatch):
        """Test for unknown location in get_address_geolocation method."""
        def mockreturn(request, key, method):
            json = {"results": [], "status": "ZERO_RESULTS"}
            return Mock(json=json)
        monkeypatch.setattr(classes.geocoder, 'google', mockreturn)
        with pytest.raises(classes.UnknownLocation):
            classes.GoogleMapsApi('hdzkjehkd').get_address_geolocation()


class TestMediaWikiApi():
    """Test for MediaWikiApi class."""

    def test_request(self, monkeypatch):
        """Test for request_wiki_page method."""
        def mockreturn(request, params):
            json = {
                    'query': {'geosearch': [{
                                            'pageid': 12,
                                            'title': 'Tour Eiffel'
                                            }]}
            }
            mock = Mock()
            mock.json.return_value = json
            return mock
        monkeypatch.setattr(classes, 'get', mockreturn)
        coordinates_input = classes.MediaWikiApi(classes.maps)
        assert coordinates_input.request_wiki_page() == (12, 'Tour Eiffel')

    def test_summary(self, monkeypatch):
        """Test for request_wiki_summary method."""
        def mockreturn(request, params):
            json = {'query': {'pages': {'1359783': {'extract': 'spam'}}}}
            mock = Mock()
            mock.json.return_value = json
            return mock
        monkeypatch.setattr(classes, 'get', mockreturn)
        assert classes.MediaWikiApi.request_wiki_summary(1359783) == 'spam'

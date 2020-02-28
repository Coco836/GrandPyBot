import program
import pytest
import GrandPyBot.config as config
import urllib.request
from unittest.mock import Mock


class TestGrandPyBotConversation:
    """docstring for GrandPyBotQuestions."""

    def test_random_responses(self):
        test_random_response = program.GrandPyBotConversation.random_response()
        assert test_random_response in program.GrandPyBotConversation.responses

    def test_random_stories_introduction(self):
        test_random_story_intro = program.GrandPyBotConversation.random_story()
        assert test_random_story_intro in program.GrandPyBotConversation.stories_intro

    def test_random_end_stories_quote(self):
        test_random_end_story_quote = program.GrandPyBotConversation.random_end_quote()
        assert test_random_end_story_quote in program.GrandPyBotConversation.end_quotes


class TestParser:
    """docstring for TestParser."""

    def test_letter_case(self):
        test_phrase = program.Parser.arrange_input('Avenue Champs-Elysées Paris France')
        assert test_phrase == 'avenue champs elysées paris france'

    def test_stopwords(self):
        test_quote = program.Parser.arrange_input("Salut GrandPy, Est-ce que tu connais adresse d'OpenClassrooms?")
        assert test_quote == "salut grandpy connais adresse openclassrooms"

class TestGoogleMapsApi():
    """docstring for TestGoogleMapsApi."""

    def test_geocode(self, monkeypatch):
        coordinates = program.GoogleMapsApi('tour eiffel')
        address_details = {
                 "formatted_address" : "Champ de Mars, 5 Avenue Anatole France"
                 ", 75007 Paris, France",
                 "geometry" : {
                    "location" : {
                       "lat" : 48.85837009999999,
                       "lng" : 2.2944813
                    },
                 },
                 "place_id" : "ChIJLU7jZClu5kcR4PcOOO6p3I0",
        }
        def mockreturn(request):
            return address_details
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)
        assert coordinates.get_address_geolocation() == (
                address_details['geometry']['location']['lat'],
                address_details['geometry']['location']['lng'],
                address_details['formatted_address']
        )
    
    def test_try_block(self):
        with pytest.raises(TypeError):
            program.GoogleMapsApi.get_address_geolocation()

    class TestMediaWikiApi():
        """docstring for TestMediaWikiApi."""

        def test_request(self, monkeypatch):
            def mockreturn(request, params):
                json = {'query' : {'geosearch' : [{'pageid': 12}]}}
                mock = Mock()
                mock.json.return_value = json
                return mock
            monkeypatch.setattr(program, 'get', mockreturn)
            coordinates_input = program.MediaWikiApi(program.maps)
            assert coordinates_input.request_wiki_page_id() == 12

        def test_summary(self, monkeypatch):
            def mockreturn(request, params):
                json = {'query' : {'pages' : {'1359783':{'extract' : 'spam'}}}}
                mock = Mock()
                mock.json.return_value = json
                return mock
            monkeypatch.setattr(program, 'get', mockreturn)
            assert program.MediaWikiApi.request_wiki_summary(1359783) == 'spam'

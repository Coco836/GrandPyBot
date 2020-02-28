import stopwords
import sys
sys.path.append("..")
import GrandPyBot.config as config
import re
import random
import geocoder
from requests import get


class GrandPyBotConversation:
    """docstring for GrandPyBotConversation."""

    responses = config.RESPONSES
    stories_intro = config.STORIES_INTRODUCTION
    end_quotes = config.END_STORIES_QUOTE

    @staticmethod
    def random_response():
        random_quote_response = random.choice(GrandPyBotConversation.responses)
        return random_quote_response

    @staticmethod
    def random_story():
        random_story_intro = random.choice(GrandPyBotConversation.stories_intro)
        return random_story_intro

    @staticmethod
    def random_end_quote():
        random_end_story_quote = random.choice(GrandPyBotConversation.end_quotes)
        return random_end_story_quote


class Parser:
    """docstring for Parser."""

    @staticmethod
    def arrange_input(sentence):
        stop_words = config.FRENCH_STOP_WORDS

        lowercase_sentence = sentence.lower()
        remove = re.sub(r"[-&_,;!?./\']", " ", lowercase_sentence).split()
        filter_sentence = [word for word in remove if word not in stop_words]
        sentence = " ".join(filter_sentence)
        return sentence

class GoogleMapsApi():
    """docstring for GoogleMapsApi."""

    def __init__(self, request):
        self.request = request
        self.latitude = 0
        self.longitude = 0
        self.address = ''

    def get_address_geolocation(self):
        request_data = geocoder.google(
                                        self.request,
                                        key=config.API_KEY_GOOGLE_MAPS
        )
        address_details = request_data.json
        try:
            self.longitude, self.latitude, self.address = (
                                                          address_details['lng'],
                                                          address_details['lat'],
                                                          address_details['address']
            )
        except TypeError:
            raise UnknownLocation

        # print(self.latitude, self.longitude, self.address)
        return self.latitude, self.longitude, self.address

class UnknownLocation(Exception):
    """Error if location not found."""


class MediaWikiApi():
    """docstring for MediaWikiApi."""

    def __init__(self, maps):
        self.coordinates = maps.get_address_geolocation()


    def request_wiki_page_id(self):
        search_params = {
                        'action': 'query',
                        'list': 'geosearch',
                        'gscoord': '{0}|{1}'.format(self.coordinates[0], self.coordinates[1]),
                        'gslimit': 1,
                        'gsradius': 10000,
                        'format': 'json'
        }
        request_wiki_data = get('https://fr.wikipedia.org/w/api.php', params=search_params)
        page_data = request_wiki_data.json()
        page_id = page_data["query"]["geosearch"][0]["pageid"]
        return page_id

    @staticmethod
    def request_wiki_summary(page_id=None):
        if not page_id:
            return "Tu es mal tombé aujourd'hui ! Je n'ai aucune histoire pour toi !"
        search_params = {
                        'action': 'query',
                        'prop': 'extracts',
                        'pageids': page_id,
                        'exlimit' : 1,
                        'explaintext' : True,
                        'exsentences': 3,
                        'format': 'json'
        }
        request_story_wiki = get('https://fr.wikipedia.org/w/api.php', params=search_params)
        story_data = request_story_wiki.json()
        story_for_location = story_data["query"]["pages"][str(page_id)]['extract']
        return story_for_location

maps = GoogleMapsApi('tour eiffel')
story = MediaWikiApi(maps)
page_id = story.request_wiki_page_id()
story.request_wiki_summary(page_id)

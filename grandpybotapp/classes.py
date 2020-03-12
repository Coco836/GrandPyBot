# import .config
import re
import random
import geocoder
from requests import get


class GrandPyBotConversation:
    """Retrieve sentences for Papy Bot answers."""

    responses = config.RESPONSES
    stories_intro = config.STORIES_INTRODUCTION
    end_quotes = config.END_STORIES_QUOTE

    @staticmethod
    def random_response():
        """Choose randomly a quote that will introduce papy bot response."""
        random_quote_response = random.choice(GrandPyBotConversation.responses)
        return random_quote_response

    @staticmethod
    def random_story():
        """
        Choose randomly a story that will introduce papy bot story
        about a place.
        """
        random_story_intro = random.choice(
                                        GrandPyBotConversation.stories_intro
        )
        return random_story_intro

    @staticmethod
    def random_end_quote():
        """Choose randomly a quote that will end the current discussion."""
        random_end_story_quote = random.choice(
                                        GrandPyBotConversation.end_quotes
        )
        return random_end_story_quote


class Parser:
    """Clear user input to keep only the key words (address)."""

    @staticmethod
    def arrange_input(sentence):
        """Method that clear input."""
        stop_words = config.FRENCH_STOP_WORDS

        # Lowercase each words
        lowercase_sentence = sentence.lower()
        # Remove, replace special characters and split the sentence
        remove = re.sub(r"[-&_,;!?./\']", " ", lowercase_sentence).split()
        # Filter the sentence by removing the words found in stop_words list
        filter_sentence = [word for word in remove if word not in stop_words]
        # Join the remaining words together
        sentence = " ".join(filter_sentence)
        return sentence


class GoogleMapsApi():
    """Retrieve data from Google Maps API."""

    def __init__(self, request):
        self.request = request
        self.latitude = 0
        self.longitude = 0
        self.address = ''

    def get_address_geolocation(self):
        """Method allowing the program to search for a specific place."""
        # Parameters request(user_input), Api key and method places needed
        # to find a specific place.
        request_data = geocoder.google(
                                        self.request,
                                        key=config.API_KEY_GOOGLE_MAPS,
                                        method="places"
        )
        # Retrieving data as .json
        address_details = request_data.json
        # Raise an error if the location requested hasn't been found
        try:
            self.longitude, self.latitude, self.address = (
                                                    address_details['lng'],
                                                    address_details['lat'],
                                                    address_details['address']
            )
        except (TypeError, KeyError):
            raise UnknownLocation

        return self.latitude, self.longitude, self.address


class UnknownLocation(Exception):
    """Error if location not found."""


class MediaWikiApi():
    """Retrieve data from Media Wiki API."""

    def __init__(self, maps):
        # Call method to retrieve the place's coordinates
        self.coordinates = maps.get_address_geolocation()

    def request_wiki_page(self):
        """Method searching for a page id and a title of a wiki article."""
        # Searching parameters for wiki_api
        search_params = {
                        'action': 'query',
                        'list': 'geosearch',
                        'gscoord': '{0}|{1}'.format(self.coordinates[0],
                                                    self.coordinates[1]),
                        'gslimit': 1,
                        'gsradius': 10000,
                        'format': 'json'
        }
        request_wiki_data = get(
                                'https://fr.wikipedia.org/w/api.php',
                                params=search_params
        )
        # Transform request data into json
        page_data = request_wiki_data.json()
        # Scan dictionary and only retrieve the two needed data
        page_id = page_data["query"]["geosearch"][0]["pageid"]
        title = page_data["query"]["geosearch"][0]["title"]
        return page_id, title

    @staticmethod
    def request_wiki_summary(page_id=None):
        """Method searching for a summary of the requested place."""
        if not page_id:
            return "Je n'ai aucune histoire pour toi !"
        # Searching parameters for wiki_summary
        search_params = {
                        'action': 'query',
                        'prop': 'extracts',
                        'pageids': page_id,
                        'exlimit': 1,
                        'explaintext': True,
                        'exsentences': 2,
                        'format': 'json'
        }
        request_story_wiki = get(
                                'https://fr.wikipedia.org/w/api.php',
                                params=search_params
        )
        # Transform request data into json
        story_data = request_story_wiki.json()
        # Scan dictionary and only retrieve the needed data
        story_for_location = (
                            story_data["query"]["pages"]
                            [str(page_id)]['extract']
        )
        return story_for_location

maps = GoogleMapsApi('tour eiffel')
story = MediaWikiApi(maps)
page = story.request_wiki_page()
story.request_wiki_summary(page[0])

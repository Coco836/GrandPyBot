#! /usr/bin/env python

from flask import Flask, render_template, url_for, request, jsonify
from .classes import (
                    Parser, GrandPyBotConversation, 
                    GoogleMapsApi, MediaWikiApi, UnknownLocation
)

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/', methods=['POST'])
def location_request():
    # Retrieve input from form.
    user_input = request.form['user_input']
    # Parse the input
    parsed_user_input = Parser.arrange_input(user_input)

    # Instanciation of GoogleMapsApi class and send parsed input
    maps = GoogleMapsApi(parsed_user_input)
    # If a location exists for the user's input return a story, a map, an url..
    # If no location exists return a simple message
    try:
        story = MediaWikiApi(maps)
    except UnknownLocation:
        message = (
                    "Je ne sais pas de quoi tu parles petit ! "
                    "Pose moi une vraie question."
        )
    else:
        address_introduction = GrandPyBotConversation.random_response()
        message = address_introduction + maps.address
        lat = maps.latitude
        lng = maps.longitude

        if message:
            page = story.request_wiki_page()
            page_title = page[1].replace(" ", "_")
            wiki_page_url = f'''https://fr.wikipedia.org/wiki/{page_title}'''
            address_story = (
                            GrandPyBotConversation.random_story() +
                            story.request_wiki_summary(page[0]) + ".. "
            )
            end_quote = GrandPyBotConversation.random_end_quote()
            return jsonify(
                            {
                                'user_input': user_input,
                                'message': message,
                                'address_story': address_story,
                                'wiki_page_url': wiki_page_url,
                                'end_quote': end_quote,
                                'latitude': lat,
                                'longitude': lng
                            }
            )

    return jsonify({'user_input': user_input, 'message': message})

if __name__ == "__main__":
    app.run(debug=True)

#! /usr/bin/env python

from flask import Flask, render_template, url_for, request, jsonify
from program import Parser, GrandPyBotConversation, GoogleMapsApi, MediaWikiApi, UnknownLocation

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/',methods = ['POST'])
def location_request():
    user_input = request.form['user_input']
    parsed_user_input = Parser.arrange_input(user_input)

    maps = GoogleMapsApi(parsed_user_input)
    try:
        story = MediaWikiApi(maps)
    except UnknownLocation:
        message = "Je ne sais pas de quoi tu parles petit ! Pose moi une vraie question."
    else:
        address_introduction = GrandPyBotConversation.random_response()
        message = address_introduction + maps.address
        if message:
            page_id = story.request_wiki_page_id()
            address_story = story.request_wiki_summary(page_id)
            return jsonify({'user_input' : user_input})
            # return render_template("index.html", user_input=user_input, message=message, address_story=address_story)
    return jsonify({'user_input' : user_input})
    # return render_template("index.html", user_input=user_input, message=message)

if __name__ == "__main__":
    app.run(debug=True)

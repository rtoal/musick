# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
from google.appengine.api import users
from artist_service import artist_info

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        nickname = None
        if user:
            nickname = user.nickname()
            auth_url = users.create_logout_url('/')
        else:
            auth_url = users.create_login_url('/')
        welcome_template = jinja_env.get_template("templates/welcome.html")
        self.response.write(welcome_template.render({
            "nickname": nickname,
            "auth_url": auth_url,
            "auth_text": "Sign out" if user else "Sign in",
        }))

class ArtistsHandler(webapp2.RequestHandler):
    def get(self):
        artists_template = jinja_env.get_template(
            "templates/artists.html")
        self.response.write(artists_template.render())

class GoodbyeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Sorry to see you go")

class ArtistHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("name")
        artist_template = jinja_env.get_template("templates/artist.html")
        self.response.write(artist_template.render({
            "name": name,
            "image": artist_info[name]['image'],
            "spotify_link": artist_info[name]['spotify_link']}))

app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/artists', ArtistsHandler),
    ('/artist', ArtistHandler),
    ('/goodbye', GoodbyeHandler),
], debug=True)

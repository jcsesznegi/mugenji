#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import cgi
import wsgiref.handlers
import os
import sys
import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

# Helper Classes
from xml.dom.minidom import parse, Node
#from pprint import pprint

# Model Classes
from kanji import Kanji
from statistics import Statistics
from user import User

# Base Classes
import mugenjiForms, mugenjiUsers
import mugenjiDb

# Pages
from pages.kanjiPages import KanjiInsertPage, KanjiReadPage, KanjiDeletePage, KanjiCardsPage, KanjiGet, KanjiFetch
from pages.userPages import UserAddKanji, UserDeleteKanji, UserStatsPage
from pages.adminPages import AdminPage, AdminDeletePage, AdminLoadPage


class MainPage(webapp.RequestHandler):
  def get(self):
    greeting = mugenjiUsers.User().greeting()
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
    self.response.out.write(template.render(path, template_values))


class SettingsPage(webapp.RequestHandler):
  def get(self):
    greeting = mugenjiUsers.User().greeting()
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
#    theme = self.request.cookies.get('theme','')
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
    self.response.out.write(template.render(path, template_values))
  def post(self):
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    theme = self.request.get('theme','')
    hidePreview = self.request.get('hidePreview','')
    greeting = mugenjiUsers.User().greeting()
    if theme is not None and hidePreview is not None:
        User().update(mugenjiUsers.User().getEmail(), theme, hidePreview)
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
#        expires = datetime.datetime.now() + datetime.timedelta(730)
#        cookie = {'theme' : theme, 'expires' : expires.strftime("%a, %d %b %Y %H:00:00 GMT")}
#        header = str('theme=' + cookie['theme'] + '; expires=' + cookie['expires'])  
#        self.response.headers.add_header('Set-Cookie', header)
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
    self.response.out.write(template.render(path, template_values))


class StatsPage(webapp.RequestHandler):
  def get(self):
    greeting = mugenjiUsers.User().greeting()
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    stats = Statistics().fetch()
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
        'stats': stats
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/stats.html')
    self.response.out.write(template.render(path, template_values))



def main():
  application = webapp.WSGIApplication([('/',                MainPage),
                                        ('/kanji/insert',    KanjiInsertPage),
                                        ('/kanji/cards',     KanjiCardsPage),
                                        ('/kanji/delete',    KanjiDeletePage),
                                        ('/kanji/get',       KanjiGet),
                                        ('/kanji/fetch' ,    KanjiFetch),
                                        ('/kanji/read',      KanjiReadPage),
                                        ('/admin/load',      AdminLoadPage),
                                        ('/admin/delete',    AdminDeletePage),
                                        ('/admin/admin',     AdminPage),
                                        ('/user/addkanji',   UserAddKanji),
                                        ('/user/deletekanji', UserDeleteKanji),
                                        ('/user/stats',      UserStatsPage),
                                        ('/stats',           StatsPage),
                                        ('/settings',        SettingsPage),
                                        ],
                                        debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__=="__main__":
  main()

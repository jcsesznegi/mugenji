
import cgi
import os
import sys
import wsgiref.handlers
import datetime


from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

# Helper Classes
from xml.dom.minidom import parse, Node, getDOMImplementation

from kanji import Kanji
from user import User

import mugenjiForms, mugenjiUsers
import mugenjiDb


class KanjiReadPage(webapp.RequestHandler):
  def get(self):
    greeting = mugenjiUsers.User().greeting()
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    key = self.request.get("key")
    kanji = Kanji().get(key)
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
        'kanji': kanji
    }
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'kanji', 'read.html')
    self.response.out.write(template.render(path, template_values))


class KanjiDeletePage(webapp.RequestHandler):
  def get(self):
    deleteKanji = self.request.get("kanji")
    try:
        kanji = Kanji().get(deleteKanji)
        db.delete(kanji)
        self.redirect('/admin/admin')
    except:
        self.redirect('/admin/admin')


class KanjiCardsPage(webapp.RequestHandler):
  def get(self):
    reqLevel = self.request.get("level")
    reqOffset = self.request.get("offset")
    level = 0
    offset = 0
    try: 
        if len(reqLevel) > 0:
            level = int(reqLevel)
        if len(reqOffset) > 0:    
            offset = int(reqOffset)
        kanjis = Kanji().fetch(level, 10, offset)
    except:
        kanjis = Kanji().fetch(0, 10)
    if kanjis.count() is 0:
        kanjis = None
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    kanjiList = []
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    for kanji in kanjis:
        hasKanji = False
        if isLoggedIn:
            for k in user.kanjiList:
                if kanji.key() == k.kanji.key():
                    hasKanji = True                
        kanjiList.append({ 'key' : kanji.key(),
                           'kanji': kanji.kanji,
                           'onYomi': kanji.onYomi,
                           'kunYomi': kanji.kunYomi,
                           'strokes': kanji.strokes,
                           'meaning': kanji.meaning,
                           'hasKanji': hasKanji
                         })
    template_values = {
        'isLoggedIn': isLoggedIn,
        'kanjiList': kanjiList
    }
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'kanji', 'cards.html')
    self.response.out.write(template.render(path, template_values))


class KanjiInsertPage(webapp.RequestHandler):
  def get(self):
    greeting = mugenjiUsers.User().greeting()
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    kanjiForm = mugenjiForms.Kanji()
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
        'kanjiForm': kanjiForm
    }
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'kanji', 'insert.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    data = mugenjiForms.Kanji(data=self.request.POST)
    if data.is_valid():
        entity = data.save(commit=True)
        self.redirect('/')
    else:
        greeting = mugenjiUsers.User().greeting() 
        isAdmin = mugenjiUsers.User().isAdmin()
        isLoggedIn = mugenjiUsers.User().isLoggedIn()
        user = None
        if isLoggedIn:
            user = User().get(mugenjiUsers.User().getEmail())
        kanjiForm = mugenjiForms.Kanji()
        template_values = {
            'isAdmin': isAdmin,
            'isLoggedIn': isLoggedIn,
            'user': user,
            'greeting': greeting, 
            'kanjiForm': data
        }
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'kanji', 'insert.html')
        self.response.out.write(template.render(path, template_values))

class KanjiGet(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    kanji = Kanji().get(key)
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "kanji", None)
    top_element = doc.documentElement
    text = doc.createTextNode(kanji.kanji)
    top_element.appendChild(text)

    self.response.out.write(doc.toxml())


class KanjiFetch(webapp.RequestHandler):
  def post(self):
    key = self.request.post('key')
    kanji = Kanji().get(key)
    self.response.out.write(kanji.kanji)








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
from xml.dom.minidom import parse, Node

from kanji import Kanji
from statistics import Statistics

import mugenjiForms, mugenjiUsers
import mugenjiDb


class AdminPage(webapp.RequestHandler):
  def get(self):
    reqLevel = self.request.get("level")
    greeting = mugenjiUsers.User().greeting()    
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
    try: 
        reqLevel = int(reqLevel)
        kanjis = Kanji().fetch(reqLevel, 50)
    except:
        kanjis = Kanji().fetch(0, 50)
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
        'kanjis': kanjis
    }
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'admin', 'admin.html')
    self.response.out.write(template.render(path, template_values))


class AdminLoadPage(webapp.RequestHandler):
  def getText(self, nodeList):
    t = []
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE:
            t.append(node.data)
    return ''.join(t)

  def get(self):
    greeting = mugenjiUsers.User().greeting()    
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())

#    dom1 = parse(os.path.join(os.path.dirname(__file__), '..', 'data', 'kanjidic2.xml'))
    dom1 = parse(os.path.join(os.path.dirname(__file__), '..', 'data', 'test.xml'))
    characters = dom1.getElementsByTagName('character')
    levelCount = {1:0,2:0,3:0,4:0,5:0}
    for character in characters:
        kanjiName  = None
        onYomi     = None
        kunYomi    = None
        meaning    = None
        strokes    = None
        note       = None
        jlptLevel  = None
        for param in character.childNodes:
            if param.nodeType == Node.ELEMENT_NODE:
                if param.localName == 'literal':
                    kanjiName = self.getText(param.childNodes)
                elif param.localName == 'misc':
                    for p in param.childNodes:
                        if p.localName == 'stroke_count':
                            strokes = int(self.getText(p.childNodes))
                        if p.localName == 'jlpt':
                            jlptLevel = int(self.getText(p.childNodes))
                elif param.localName == 'reading_meaning':
                    for p in param.childNodes:
                        if p.localName == 'rmgroup':
                            m = []
                            o = []
                            k = []
                            for p2 in p.childNodes: 
                                if p2.localName == 'meaning' and not p2.attributes.keys():
                                    m.append(self.getText(p2.childNodes))
                                if p2.localName == 'reading' and p2.attributes['r_type']:
                                    if p2.attributes['r_type'].value == 'ja_on':
                                         o.append(self.getText(p2.childNodes))
                                if p2.localName == 'reading' and p2.attributes['r_type']:
                                    if p2.attributes['r_type'].value == 'ja_kun':
                                        k.append(self.getText(p2.childNodes))
                            meaning = ', '.join(m)
                            onYomi = ', '.join(o)
                            kunYomi = ', '.join(k)
        Kanji().put(kanjiName, meaning, strokes, jlptLevel, onYomi, kunYomi)
        if jlptLevel in levelCount:
            levelCount[jlptLevel] = levelCount[jlptLevel] + 1 
    for n, v in levelCount.items():
        Statistics().put('levelCount'+str(n), v)
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'greeting': greeting,
    }

    self.redirect('/admin/admin')


class AdminDeletePage(webapp.RequestHandler):
  def get(self):
    results = Kanji().fetch(0)
    for result in results:
        result.delete()
    self.redirect('/admin/admin')




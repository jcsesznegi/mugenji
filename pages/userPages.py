
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

from user import User
from statistics import Statistics

import mugenjiForms, mugenjiUsers
import mugenjiDb


class UserAddKanji(webapp.RequestHandler):
  def post(self):
      email = mugenjiUsers.User().getEmail()
      kanji = self.request.get("kanji")
      if email is not None and kanji is not None:
          User().putKanji(email, kanji)


class UserDeleteKanji(webapp.RequestHandler):
  def post(self):
      email = mugenjiUsers.User().getEmail()
      kanji = self.request.get("kanji")
      if email is not None and kanji is not None:
          User().deleteKanji(email, kanji)


class UserStatsPage(webapp.RequestHandler):
  def get(self):
    isAdmin = mugenjiUsers.User().isAdmin()
    isLoggedIn = mugenjiUsers.User().isLoggedIn()
    totalCount = None
    user = None
    if isLoggedIn:
        user = User().get(mugenjiUsers.User().getEmail())
        completion = User().getCompletion(mugenjiUsers.User().getEmail())
        level1 = completion['level1']
        level2 = completion['level2']
        level3 = completion['level3']
        level4 = completion['level4']
        level5 = completion['level5']
        levelAll = level1 + level2 + level3 + level4 + level5
        level1Total = int(Statistics().getValue('levelCount1'))
        level2Total = int(Statistics().getValue('levelCount2'))
        level3Total = int(Statistics().getValue('levelCount3'))
        level4Total = int(Statistics().getValue('levelCount4'))
        level5Total = int(Statistics().getValue('levelCount5'))
        levelAllTotal = level1Total + level2Total + level3Total + level4Total + level5Total
        if level1 == 0 or level1Total == 0:
            level1Ratio = '-'
        else:
            level1Ratio = round(level1 / level1Total, 2)
        if level2 == 0 or level2Total == 0:
            level2Ratio = '-'
        else:
            level2Ratio = round(level2 / level2Total, 2)
        if level3 == 0 or level3Total == 0:
            level3Ratio = '-'
        else:
            level3Ratio = round(level3 / level3Total, 2)
        if level4 == 0 or level4Total == 0:
            level4Ratio = '-'
        else:
            level4Ratio = round(level4 / level4Total, 2)
        if level5 == 0 or level5Total == 0:
            level5Ratio = '-'
        else:
            level5Ratio = round(level5 / level5Total, 2)
        if levelAll == 0 or levelAllTotal == 0:
            levelAllRatio = '-'
        else:
            levelAllRatio = round(levelAll / levelAllTotal, 2)
        totalCount = { 'level1'        : level1,
                       'level2'        : level2,
                       'level3'        : level3,
                       'level4'        : level4,
                       'level5'        : level5,
                       'levelAll'      : levelAll,
                       'level1Total'   : level1Total,
                       'level2Total'   : level2Total,
                       'level3Total'   : level3Total,
                       'level4Total'   : level4Total,
                       'level5Total'   : level5Total,
                       'levelAllTotal' : levelAllTotal,
                       'level1Ratio'   : level1Ratio,
                       'level2Ratio'   : level2Ratio,
                       'level3Ratio'   : level3Ratio,
                       'level4Ratio'   : level4Ratio,
                       'level5Ratio'   : level5Ratio,
                       'levelAllRatio' : levelAllRatio
                     }
    template_values = {
        'isAdmin': isAdmin,
        'isLoggedIn': isLoggedIn,
        'user': user,
        'totalCount': totalCount
    }
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'user', 'stats.html')
    self.response.out.write(template.render(path, template_values))





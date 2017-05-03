
from google.appengine.ext import db
import mugenjiDb

import datetime

class User():
  def get(self, email):
      if not self.exists(email):        
          self.put(email)
      sql = "SELECT * FROM User WHERE email = :1"
      query = db.GqlQuery(sql, email)
      result = query.get()
      return result

  def put(self, email):
      u = mugenjiDb.User()
      u.email         = email
      u.insertDate    = datetime.datetime.now() 
      u.lastLogin     = datetime.datetime.now()
      u.hidePreview   = False
      u.theme         = "default" 
      u.put() 

  def putKanji(self, email, kanji):
      # get user
      sql = "SELECT * FROM User WHERE email = :1"
      query = db.GqlQuery(sql, email)
      u = query.get()
      # get kanji
      kDb = mugenjiDb.Kanji()
      k = kDb.get(kanji)
      # put user kanji
      mugenjiDb.UserKanji(user=u, kanji=k).put()
      return True

  def deleteKanji(self, email, kanji):
      # get user
      sql = "SELECT * FROM User WHERE email = :1"
      query = db.GqlQuery(sql, email)
      u = query.get()
      deleteKey = None
      for k in u.kanjiList:
          if str(k.kanji.key()) == kanji:
              deleteKey = str(k.key())
      # get kanji
      if deleteKey is not None:
          ukDb = mugenjiDb.UserKanji()
          d = ukDb.get(deleteKey)
          d.delete()
          return True
      return False

  def getCompletion (self, email):
      # get user
      sql = "SELECT * FROM User WHERE email = :1"
      query = db.GqlQuery(sql, email)
      user = query.get()
      level1 = 0
      level2 = 0
      level3 = 0
      level4 = 0
      level5 = 0
      for k in user.kanjiList:  
          if k.kanji.jlptLevel == 1:
              level1 += 1 
          if k.kanji.jlptLevel == 2:
              level1 += 1 
          if k.kanji.jlptLevel == 3:
              level1 += 1 
          if k.kanji.jlptLevel == 4:
              level1 += 1 
          if k.kanji.jlptLevel == 5:
              level1 += 1 
      completion = {'level1' : level1,
                    'level2' : level2,
                    'level3' : level3,
                    'level4' : level4,
                    'level5' : level5 }
      return completion

  def update(self, email, theme, hidePreview):
      user = self.get(email)
      user.theme = theme
      if hidePreview == 'True':
          user.hidePreview = True
      if hidePreview == 'False':
          user.hidePreview = False
      user.put()
      return True

  def exists(self, email):
      sql = "SELECT * FROM User WHERE email = :1"
      query = db.GqlQuery(sql, email)
      result = query.get()
      if result is not None:
          return True
      else:
          return False

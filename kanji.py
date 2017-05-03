
from google.appengine.ext import db
import mugenjiDb

class Kanji():
  def fetch(self, level, limit = None, offset = None):
      sql = "SELECT * FROM Kanji"
      if level > 0:
          sql += " WHERE jlptLevel = "
          sql += str(level)
      if limit is not None:
          sql += " LIMIT "
          sql += str(limit)
      if offset is not None:
          sql += " OFFSET "
          sql += str(offset)
      result = db.GqlQuery(sql)
      return result

  def get(self, kanji):
      k = mugenjiDb.Kanji()
      result = k.get(kanji)
      return result

  def put(self, name, meaning, strokes, level, onYomi, kunYomi):
      k = mugenjiDb.Kanji()
      k.kanji      = name
      k.meaning    = meaning
      k.strokes    = strokes
      k.jlptLevel  = level
      k.onYomi     = onYomi
      k.kunYomi    = kunYomi
      k.put() 



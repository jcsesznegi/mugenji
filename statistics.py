
from google.appengine.ext import db
import mugenjiDb

class Statistics():
  def fetch(self, limit = None, offset = None):
      sql = "SELECT * FROM Statistics"
      if limit is not None:
          sql += " LIMIT "
          sql += str(limit)
      if offset is not None:
          sql += " OFFSET "
          sql += str(offset)
      result = db.GqlQuery(sql)
      return result

  def get(self, name):
      sql = "SELECT * FROM Statistics WHERE name = :1"
      query = db.GqlQuery(sql, name)
      result = query.get()
      return result

  def getValue(self, name):
      result = self.get(name)
      return result.value

#  def getKanjiCountTotal(self):
#      total = int(self.getValue('levelCount1')) + int(self.getValue('levelCount2')) + int(self.getValue('levelCount3')) + int(self.getValue('levelCount4')) + int(self.getValue('levelCount5')) 
#      return total

  def increment(self, name):
      sql = "SELECT * FROM Statistics where name = "
      sql += name
      stats = db.GqlQuery(sql)
      for stat in stats:
          stat.value = stat.value + 1
      return true

  def put(self, name, value):
      s = mugenjiDb.Statistics()
      s.name      = name
      s.value     = value
      s.put() 



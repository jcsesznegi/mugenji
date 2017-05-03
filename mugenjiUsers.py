from google.appengine.api import users

class User():
  def greeting(self):
      user = users.get_current_user()
      if user:
          greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                      (user.nickname(), users.create_logout_url("/")))
      else:
          greeting = ("<a href=\"%s\">Sign in or register</a>." %
                      users.create_login_url("/"))
      return greeting

  def getEmail(self):
      user = users.get_current_user()
      if user:        
          return user.email()
      else:
          return False


  def isLoggedIn(self):
      user = users.get_current_user()
      if user:
          return True
      else:
          return False


  def isAdmin(self):
      return users.is_current_user_admin()



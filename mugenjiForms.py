
from google.appengine.ext.db import djangoforms
import mugenjiDb

class Kanji(djangoforms.ModelForm):
  class Meta:
    model = mugenjiDb.Kanji


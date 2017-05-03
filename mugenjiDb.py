
from google.appengine.ext import db

class User(db.Model):
    email                    = db.EmailProperty()
    insertDate               = db.DateTimeProperty()
    lastLogin                = db.DateTimeProperty()
    hidePreview              = db.BooleanProperty()
    theme                    = db.StringProperty()


class Statistics(db.Model):
    name                     = db.StringProperty()
    value                    = db.IntegerProperty()

class Kanji(db.Model):
    kanji                    = db.StringProperty()
    onYomi                   = db.StringProperty()
    kunYomi                  = db.StringProperty()
    meaning                  = db.StringProperty()
    strokes                  = db.IntegerProperty()
    note                     = db.StringProperty()
    jlptLevel                = db.IntegerProperty()


class UserKanji(db.Model):
    user                     = db.ReferenceProperty(User, collection_name='kanjiList')
    kanji                    = db.ReferenceProperty(Kanji, collection_name='userList')


class Radical(db.Model):
    radical                  = db.StringProperty()
    meaning                  = db.StringProperty()


class KanjiRadical(db.Model):
    kanji                    = db.ReferenceProperty(Kanji)
    radical                  = db.ReferenceProperty(Radical)


class Word(db.Model):
    kanji                    = db.ReferenceProperty(Kanji)
    word                     = db.StringProperty()
    wordRomaji               = db.StringProperty()
    meaning                  = db.StringProperty()


class Sentence(db.Model):    
    kanji                    = db.ReferenceProperty(Kanji)
    sentence                 = db.StringProperty()
    sentenceRomaji           = db.StringProperty()
    meaning                  = db.StringProperty()

































































from google.appengine.ext import db

class UserPreference(db.Model):
    user = db.UserProperty()
    # The format of this field is YYYYWW where YYYY is the 4 digit
    # year and WW is the 2 digit week number.
    last_update_week_id = db.StringProperty()

class WeekUpdate(db.Model):
    submit_date = db.DataProperty()
    body = db.StringProperty()

def get_user_preference(email_address):
    pass

def get_all_user_preferences():
    pass

def get_week_updates_for_week_id(week_id):
    pass

def get_users_without_updates_for_week(week_id):
    pass

def add_week_update(user, week_id, body):
    pass

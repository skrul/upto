from datetime import datetime

from google.appengine.ext import db

class UserPreference(db.Model):
    user = db.UserProperty()
    # The format of this field is YYYYWW where YYYY is the 4 digit
    # year and WW is the 2 digit week number.
    last_update_week_id = db.StringProperty()

    @classmethod
    def get_by_email(cls, email):
        return UserPreference.get_by_key_name(email)

    @classmethod
    def get_by_user(cls, user):
        up = UserPreference.get_by_key_name(user.email())
        if up is None:
            up = UserPreference(key_name=user.email())
            up.user = user
            up.put()
        return up

    @classmethod
    def get_all(cls):
        return UserPreference.all().fetch(1000)

    @classmethod
    def get_all_without_updates_for_week(cls, week_id):
        up_keys = {}
        ups = UserPreference.all().fetch(1000)
        for up in ups:
            up_keys[str(up.key())] = up
        wus = WeekUpdate.get_all_for_week_id(week_id)
        for wu in wus:
            del up_keys[str(wu.parent().key())]
        return up_keys.values()


class WeekUpdate(db.Model):
    submit_date = db.DateTimeProperty(auto_now=True)
    user_preference = db.ReferenceProperty(UserPreference)
    week_id = db.StringProperty()
    body = db.StringProperty(multiline=True)

    @classmethod
    def current_week_id(cls):
        return datetime.now().strftime('%Y%U')

    @classmethod
    def key_for(cls, user_preference, week_id):
        key = db.Key.from_path('UserPreference', user_preference.user.email(),
                               'WeekUpdate', week_id)
        return key

    @classmethod
    def get_all_for_week_id(cls, week_id):
        return WeekUpdate.all().filter('week_id = ', week_id).fetch(1000)

    @classmethod
    def add(cls, up, week_id, body):
        wu = WeekUpdate.get_by_key_name(week_id, parent=up)
        if wu is None:
            wu = WeekUpdate(key_name=week_id, parent=up)
            wu.user_preference = up
            wu.week_id = week_id

        wu.body = body
        wu.put()

        up.last_update_week_id = week_id
        up.put()
        return wu

from google.appengine.ext import db

class UserPreference(db.Model):
    user = db.UserProperty()
    # The format of this field is YYYYWW where YYYY is the 4 digit
    # year and WW is the 2 digit week number.
    last_update_week_id = db.StringProperty()

    @classmethod
    def get_by_email(cls, email):
        pass

    @classmethod
    def get_by_user(cls, user):
        up = UserPreference.get_by_key_name(user.email())
        if up is None:
            up = UserPreference(key_name=user.email())
            up.user = user
            up.last_update_week_id = None
            db.put(up)
        return up

    @classmethod
    def get_all_user_preferences(cls):
        pass

    @classmethod
    def get_users_without_updates_for_week(cls, week_id):
        pass

class WeekUpdate(db.Model):
    submit_date = db.DateProperty()
    body = db.StringProperty()

    @classmethod
    def get_week_updates_for_week_id(cls, week_id):
        pass

    @classmethod
    def add_week_update(cls, user, week_id, body):
        pass

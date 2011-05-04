import os.path

from google.appengine.ext.webapp import template

import model

class Mail(object):
    @classmethod
    def _render(cls, tmpl, values):
        path = os.path.join(os.path.dirname(__file__), 'templates', tmpl)
        lines = template.render(path, values).split('\n')
        return (lines[0], '\n'.join(lines[1:]))

    @classmethod
    def generate_new_week_emails(cls, last_week_id):
        ups = model.UserPreference.get_all()
        for up in ups:
            last_key = model.WeekUpdate.key_for(up, last_week_id)
            wu = model.WeekUpdate.get(last_key)
            if wu is not None:
                last_body = wu.body
            else:
                last_body = 'No update last week.'

            d = dict(reminder=False, name=up.user.nickname(),
                     last_week_body=last_body)

            (subject, body) = cls._render('new_week.txt', d)
            yield (up.user.email(), subject, body)

    @classmethod
    def generate_reminder_emails(cls, current_week_id, last_week_id):
        ups = model.UserPreference.get_all_without_updates_for_week(
            current_week_id)

        for up in ups:
            last_key = model.WeekUpdate.key_for(up, last_week_id)
            wu = model.WeekUpdate.get(last_key)
            if wu is not None:
                last_body = wu.body
            else:
                last_body = 'No update last week.'

            d = dict(reminder=True, name=up.user.nickname(),
                     last_week_body=last_body)

            (subject, body) = cls._render('new_week.txt', d)
            yield (up.user.email(), subject, body)

    @classmethod
    def generate_summary_emails(cls, week_id):
        wus = model.WeekUpdate.get_all_for_week_id(week_id)
        updates = []
        emails = []
        for wu in wus:
            name = wu.user_preference.user.nickname()
            email = wu.user_preference.user.email()
            body = wu.body
            updates.append(dict(name=name, email=email, body=body))
            emails.append(email)

        (subject, body) = cls._render('summary.txt', dict(updates=updates))
        for email in emails:
            yield (email, subject, body)


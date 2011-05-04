import unittest

import mail
import model

from google.appengine.ext import testbed
from google.appengine.api import users


class MailTestCase(unittest.TestCase):
  def setUp(self):
      self.testbed = testbed.Testbed()
      self.testbed.activate()
      self.testbed.init_datastore_v3_stub()

  def tearDown(self):
      self.testbed.deactivate()

  def test_generate_new_week_emails(self):
      email = 'homer@snpp.com'
      week_id = '201101'
      body = 'line1\nline2\n'
      user = users.User(email=email)
      up = model.UserPreference.get_by_user(user)
      model.WeekUpdate.add(up, week_id, body)

      l = list(mail.Mail.generate_new_week_emails(week_id))
      self.assertEqual(1, len(l))
      self.assertEqual(email, l[0][0])
      self.assertEqual('What are you up to this week?', l[0][1])
      self.assertTrue(l[0][2].find(body) > 0)

  def test_generate_reminder_emails(self):
      email = 'homer@snpp.com'
      week_id = '201101'
      body = 'line1\nline2\n'
      user = users.User(email=email)
      up = model.UserPreference.get_by_user(user)
      model.WeekUpdate.add(up, week_id, body)

      l = list(mail.Mail.generate_reminder_emails('201102', week_id))
      self.assertEqual(1, len(l))
      self.assertEqual(email, l[0][0])
      self.assertEqual('We want to know what you are up to this week.',
                       l[0][1])
      self.assertTrue(l[0][2].find(body) > 0)

  def test_generate_summary_emails(self):
      email = 'homer@snpp.com'
      week_id = '201101'
      body = 'line1\nline2\n'
      user = users.User(email=email)
      up = model.UserPreference.get_by_user(user)
      model.WeekUpdate.add(up, week_id, body)

      l = list(mail.Mail.generate_summary_emails(week_id))
      self.assertEqual(1, len(l))
      self.assertEqual(email, l[0][0])
      self.assertEqual('Everyone\'s updates for this week', l[0][1])
      self.assertTrue(l[0][2].find(body) > 0)

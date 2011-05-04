import unittest

import model

from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import users


class ModelTestCase(unittest.TestCase):
  def setUp(self):
      self.testbed = testbed.Testbed()
      self.testbed.activate()
      self.testbed.init_datastore_v3_stub()

  def tearDown(self):
      self.testbed.deactivate()

  def add_user_preference(self, email):
      user = users.User(email=email)
      up = model.UserPreference(key_name=user.email())
      up.user = user
      up.put()
      return up

  def test_get_user_preference_by_user(self):
      email = 'homer@snpp.com'
      user = users.User(email=email)
      up = model.UserPreference.get_by_user(user)
      self.assertEqual(email, up.user.email())

      up = model.UserPreference.get_by_key_name(email)
      self.assertEqual(email, up.user.email())

  def test_get_by_email(self):
      email = 'homer@snpp.com'
      up = model.UserPreference.get_by_email(email)
      self.assertTrue(up is None)

      self.add_user_preference(email)

      up = model.UserPreference.get_by_email(email)
      self.assertEqual(email, up.user.email())

  def test_get_all_user_preferences(self):
      ups = model.UserPreference.get_all();
      self.assertEqual(0, len(ups))

      email = 'homer@snpp.com'
      self.add_user_preference(email)

      ups = model.UserPreference.get_all();
      self.assertEqual(1, len(ups))
      self.assertEqual(email, ups[0].user.email())

  def test_add_week_update(self):
      email = 'homer@snpp.com'
      self.add_user_preference(email)
      up = model.UserPreference.get_by_email(email)

      week_id = '201101'
      body = 'hello world'
      uw = model.WeekUpdate.add(up, week_id, body)
      self.assertEqual(week_id, uw.week_id)
      self.assertEqual(up.user.email(), uw.user_preference.user.email())
      self.assertEqual(body, uw.body)
      self.assertEqual(up.last_update_week_id, week_id)

      body = 'hello new world'
      uw = model.WeekUpdate.add(up, week_id, body)
      self.assertEqual(week_id, uw.week_id)
      self.assertEqual(body, uw.body)
      self.assertEqual(up.last_update_week_id, week_id)

  def test_get_all_for_week_id(self):
      week_id = '201101'
      wus = model.WeekUpdate.get_all_for_week_id(week_id)
      self.assertEqual(0, len(wus))
      up1 = self.add_user_preference('homer@snpp.com')
      up2 = self.add_user_preference('marge@snpp.com')
      uw = model.WeekUpdate.add(up1, week_id, 'body1')
      uw = model.WeekUpdate.add(up2, week_id, 'body2')

      wus = model.WeekUpdate.get_all_for_week_id(week_id)
      self.assertEqual(2, len(wus))
      self.assertTrue(wus[0].body == 'body1' or wus[0].body == 'body2')
      self.assertTrue(wus[1].body == 'body1' or wus[1].body == 'body2')

  def test_get_all_without_updates_for_week(self):
      week_id = '201101'
      up1 = self.add_user_preference('homer@snpp.com')
      up2 = self.add_user_preference('marge@snpp.com')

      ups = model.UserPreference.get_all_without_updates_for_week(week_id)
      self.assertEqual(2, len(ups))

      uw = model.WeekUpdate.add(up1, week_id, 'body1')
      ups = model.UserPreference.get_all_without_updates_for_week(week_id)
      self.assertEqual(1, len(ups))

      uw = model.WeekUpdate.add(up2, week_id, 'body2')
      ups = model.UserPreference.get_all_without_updates_for_week(week_id)
      self.assertEqual(0, len(ups))

  def test_key_for_week_update(self):
      week_id = '201101'
      up = self.add_user_preference('homer@snpp.com')
      model.WeekUpdate.add(up, week_id, 'body')

      key = model.WeekUpdate.key_for(up, week_id)
      wu = model.WeekUpdate.get(key)
      self.assertEqual('body', wu.body)

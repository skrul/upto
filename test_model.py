import unittest

import model

from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import users


class DemoTestCase(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def test_get_user_preference_by_user(self):
      email = 'homer@snpp.com'
      user = users.User(email=email)
      user_preference = model.UserPreference.get_by_user(user)
      self.assertEqual(email, user_preference.user.email())

      user = model.UserPreference.get_by_key_name(email)
      self.assertTrue(user is not None)

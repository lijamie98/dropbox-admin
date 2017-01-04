from __future__ import absolute_import
import unittest

from dbadmin import dbadmin_auth


class TestStringMethods(unittest.TestCase):
    def test_with_ldap_forumsys(self):
        self.auth = dbadmin_auth.LdapAuth(
            uri='ldap://ldap.forumsys.com:389',
            base_dn='dc=example,dc=com',
            ro_account='cn=read-only-admin,dc=example,dc=com',
            ro_password='password')
        self.assertTrue(self.auth.match_user('einstein@ldap.forumsys.com', 'password'))
        self.assertTrue(self.auth.match_user('einstein', 'password'))
        self.assertTrue(self.auth.match_user('curie', 'password'))
        self.assertTrue(self.auth.match_user('curie@ldap.forumsys.com', 'password'))
        self.assertFalse(self.auth.match_user('curie@ldap.forumsys.com', 'password1'))
        self.assertFalse(self.auth.match_user('curie123', 'password'))


if __name__ == '__main__':
    unittest.main()

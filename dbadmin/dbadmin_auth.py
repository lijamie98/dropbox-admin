import ldap


class LdapAuth:
    def __init__(self, **kwargs):
        self.uri = kwargs['uri']
        self.base_dn = kwargs['base_dn']
        self.ro_account = kwargs['ro_account']
        self.ro_password = kwargs['ro_password']

    def match_user(self, user, password):
        # Search DN that matches the user
        conn = ldap.initialize(self.uri)
        # Find the DN that matches the user
        dn = self.__search_with_filter('mail', user)
        if dn is None:
            dn = self.__search_with_filter('uid', user)
        if dn is None:
            dn = self.__search_with_filter('sAMAccount', user)
        if dn is None:
            return False

        try:
            # Now bind with the searched DN with the password
            conn.bind_s(dn, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
        finally:
            if conn is not None:
                conn.unbind_s()

    def __search_with_filter(self, attr, value):
        try:
            # Search DN that matches the user
            conn = ldap.initialize(self.uri)
            search_filter = '({}={})'.format(attr, value)

            # search the DN of the email
            conn.bind_s(self.ro_account, self.ro_password)
            search_results = conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter, [""])

            if search_results is None or len(search_results) == 0:
                return None

            if len(search_results) != 1:
                raise LookupError('More than one user matches {}'.format(value))

            # returns the DN of the searched result
            return search_results[0][0]
        finally:
            if conn is not None:
                conn.unbind_s()

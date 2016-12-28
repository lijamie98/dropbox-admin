import ldap


class LdapAuth:
    def __init__(self, server_uri, base_dn):
        self.server_uri = server_uri
        self.base_dn = base_dn
        self.ldap = ldap.initialize(server_uri)

    def match_user(self, user, password):
        # create the dn for the user
        user_dn = 'uid=' + user + ',' + self.base_dn

        # noinspection PyUnresolvedReferences
        try:
            self.ldap.bind_s(user_dn, password)
            self.ldap.unbind_s()  # safely unbind
            return True
        except (AttributeError, ldap.INVALID_CREDENTIALS):  # throws AttributeError if invalid credentials
            return False

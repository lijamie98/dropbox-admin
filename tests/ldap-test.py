from dbadmin import dbadmin_auth

ldapAuth = dbadmin_auth.LdapAuth('ldap://ldap.forumsys.com:389', 'dc=example,dc=com')

print ldapAuth.match_user('einstein', 'password')

print ldapAuth.match_user('curie', 'foo')

# import ldap
#
# ld = ldap.initialize('ldap://ldap.forumsys.com:389')
#
# base_dn = 'dc=example,dc=com'
#
# user = 'curie'
# password = 'password'
#
# user_dn = 'uid=' + user + ',dc=example,dc=com'
#
# try:
#     ld.simple_bind_s(user_dn, password) # binds to see if dn and password is valid
# except ldap.INVALID_CREDENTIALS:
#     print "INCORRECT CREDENTIALS"
#
# ld.unbind()
# # ld.search_s(base_dn,)
#
# # print ld.whoami_s()

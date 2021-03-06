#!/usr/bin/env python

from globals import *
import sys

from cpanel import try_remove, force_create

# Write new globals here
moreglobals = open("moreglobals.py", "wt")

import xmlrpclib 
server = xmlrpclib.ServerProxy('https://api.webfaction.com/') 
session_id, account = server.login(USERNAME, PASSWORD)
#print >> sys.stderr, repr(session_id)
#print >> sys.stderr, repr(account)
#{'username': 'test5', 'home': '/home2', 'id': 237} 

#for i in server.list_emails(session_id):
#    print >> sys.stderr, i

if SUBDOMAINNAME is None:
    r = force_create(server, session_id, DOMAINNAME, "domain", "create_domain", "delete_domain", "list_domains", namename="domain", overwrite=False)
else:
    r = force_create(server, session_id, DOMAINNAME, "domain", "create_domain", "delete_domain", "list_domains", [SUBDOMAINNAME], namename="domain", overwrite=False)

r = force_create(server, session_id, APPNAME, "app", "create_app", "delete_app", "list_apps", ['custom_app_with_port', False, ''])
PORT = r["port"]
moreglobals.write("%s = '%s'\n" % ("PORT", PORT))

if SERVERIP is None:
    SERVERIP = server.list_websites(session_id)[0]["ip"]
    print >> sys.stderr, "No SERVERIP given. Using %s" % SERVERIP
# TODO: Add https here
# TODO: Add subdomains www and stats here
# TODO: Add path location of application here
# TODO: If the domain already exists, we should UPDATE it
r = force_create(server, session_id, WEBSITENAME, "website", "create_website", "delete_website", "list_websites",  [SERVERIP, False, [FULLDOMAINNAME], [APPNAME, URLPATH]], overwrite=False)

if DATABASEPASSWORD is None:
    import randompassword
    DATABASEPASSWORD = randompassword.GenPasswd2()
    moreglobals.write("%s = '%s'\n" % ("DATABASEPASSWORD", DATABASEPASSWORD))
    print >> sys.stderr, "No DATABASEPASSWORD given. Using %s" % DATABASEPASSWORD
assert DATABASETYPE in ["mysql", "postgresql"]
r = force_create(server, session_id, DATABASENAME, "db", "create_db", "delete_db", "list_dbs", [DATABASETYPE, DATABASEPASSWORD], delete_extra_params=[DATABASETYPE])

# TODO: Add a static media server

if MAILBOXPASSWORD is None:
    import randompassword
    MAILBOXPASSWORD = randompassword.GenPasswd2()
    moreglobals.write("%s = '%s'\n" % ("MAILBOXPASSWORD", MAILBOXPASSWORD))
    print >> sys.stderr, "No MAILBOXPASSWORD given. Using %s" % MAILBOXPASSWORD
# Annoying webfaction idiosyncracy: we have to remove the email address associated with this mailbox, or we cannot delete this mailbox
try_remove(server, session_id, EMAILADDRESS, "email", "delete_email", "list_emails", namename='email_address')
r = force_create(server, session_id, MAILBOXUSERNAME, "mailbox", "create_mailbox", "delete_mailbox", "list_mailboxes", [False, False, '', False, ''], namename='mailbox')
r = server.change_mailbox_password(session_id, MAILBOXUSERNAME, MAILBOXPASSWORD)
print >> sys.stderr, "server.change_mailbox_password: %s" % r

TARGETS = '%s,%s' % (MAILBOXUSERNAME, YOUREMAIL)
r = force_create(server, session_id, EMAILADDRESS, "email", "create_email", "delete_email", "list_emails", [TARGETS], namename='email_address')

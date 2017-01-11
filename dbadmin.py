import logging
import os

import argparse
import jsonpickle as jsonpickle
import yaml
from flask import Flask
from flask import abort
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for

from dbadmin import dbadmin_auth
from dbadmin import dbadmin_service

application = Flask(__name__)


def check_login(logged_in):
    if 'authenticated' in session:
        return logged_in
    return redirect(url_for('login'))


# define contextual processes.
@application.context_processor
def pages_json():
    return dict(pages=pagesJson)


@application.route('/')
def index():
    return check_login(render_template('index.html'))


@application.route('/shared-folders', methods=['GET'])
def list_all_shared_folders():
    if 'authenticated' in session:
        force_update = (request.args.get('force-update') == "1")
        result = service.list_all_shared_folders(force_update=force_update)
        return json.dumps(json.loads(jsonpickle.encode(result)), indent=2)
    abort(401)


@application.route('/links', methods=['GET'])
def list_all_shared_links():
    if 'authenticated' in session:
        force_update = (request.args.get('force-update') == "1")
        result = service.list_all_shared_links(force_update=force_update)
        return json.dumps(json.loads(jsonpickle.encode(result)), indent=2)
    abort(401)


@application.route('/members', methods=['GET'])
def list_all_team_members():
    if 'authenticated' in session:
        return json.dumps(json.loads(jsonpickle.encode(service.list_team_members())), indent=2)
    abort(401)


@application.route('/members/<path:team_member_id>/shared-folders', methods=['GET'])
def list_shared_folders(team_member_id):
    if 'authenticated' in session:
        return json.dumps(json.loads(jsonpickle.encode(service.list_shared_folders(team_member_id))), indent=2)
    abort(401)


@application.route('/members/<path:team_member_id>/shared-links', methods=['GET'])
def list_shared_links(team_member_id):
    if 'authenticated' in session:
        return json.dumps(json.loads(jsonpickle.encode(service.list_shared_links(team_member_id))), indent=2)
    abort(401)


@application.route('/members/<path:team_member_id>/shared-links/_revoke', methods=['DELETE'])
def revoke_shared_link(team_member_id):
    if 'authenticated' in session:
        service.revoke_shared_link(team_member_id, request.headers['url'])
        return '200', 200
    abort(401)


@application.route('/members/<path:team_member_id>/shared-folders/_unshare', methods=['DELETE'])
def unshare_folder(team_member_id):
    if 'authenticated' in session:
        service.unshare_folder(team_member_id, request.headers['shared_folder_id'])
        return '200', 200
    abort(401)


@application.route('/pages/members')
def members_page():
    return check_login(render_template('members.html'))


# user dashboard page
@application.route('/pages/dashboard')
def user_dashboard_page():
    return check_login(render_template('user-dashboard.html'))


# shared link page
@application.route('/pages/links')
def link_page():
    return check_login(render_template('links.html'))


# shared folders page
@application.route('/pages/shared-folders')
def shared_folders():
    return check_login(render_template('shared-folders.html'))


# login page
def authenticate(username, password):
    # handle login here and return a boolean
    return auth.authenticate(username, password)


@application.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html'), 302
    elif request.method == "POST":
        if authenticate(request.form['username'], request.form['password']):
            session['authenticated'] = True
            return redirect(url_for('index'), 302)
        return redirect("/login?incorrect=true")
    return None


'''

To be used in the future.

'''


@application.route('/progress', methods=['GET'])
def get_progress():
    return json.dumps(json.loads(jsonpickle.encode(service.progress)), indent=2)


@application.errorhandler(404)
def error(e):
    return render_template('error.html', status=e.code), e.code


@application.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


def create_auth(ldap_config, acl):
    return dbadmin_auth.LdapAuth(
        uri=ldap_config['uri'],
        base_dn=ldap_config['search_base_dn'],
        ro_account=ldap_config['ro_account'],
        ro_password=ldap_config['ro_password'],
        acl=acl)


if __name__ == '__main__':
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ldap", help="LDAP settings in config.yaml. Default: 'ldap'", default="ldap")
        parser.add_argument("--debug", help="Run Flask in debug mode.", action="store_true")
        args = parser.parse_args()

        # Load the configuration file
        with open('config.yaml', 'r') as token_file:
            config = yaml.load(token_file)

        # Load hte pages configuration for views.
        with open('pages.json', 'r') as f:
            pagesJson = jsonpickle.decode(f.read())

        # initialize dropbox service
        service = dbadmin_service.DropboxService(token=config['dropbox-token'])

        # initialize authentication
        auth = create_auth(config[args.ldap], config['acl'])

        application.secret_key = os.urandom(24)
        application.run(host='0.0.0.0', debug=args.debug)

    except IOError:
        logging.error("Error reading token.yaml. Please make sure the token.yaml file is properly configured.")

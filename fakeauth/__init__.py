#!/usr/bin/python
import json
import os

local_path = os.path.dirname(os.path.abspath(__file__))

# from openstack_auth import backend
from openstack_auth import user
# from openstack_dashboard.api import base
from keystoneauth1.access import access
from keystoneauth1.access import service_catalog


# class AuthRef(base.APIDictWrapper):
#     _attrs = [u'unscoped_token', u'domain', u'serviceCatalog',
#               u'roles', u'user_domain_id', u'user_domain_name',
#               u'expires', u'is_federated', u'project',
#               u'user', u'id', u'tenant', u'user_id', u'username',
#               u'auth_token']


def load_service_catalog():
    service_catalog = {}
    with open(os.path.join(local_path, 'service_catalog.json'), 'r') as f:
        service_catalog = json.load(f)
    return service_catalog


def load_auth_ref():
    auth_ref = {}
    with open(os.path.join(local_path, 'auth_ref.json'), 'r') as f:
        auth_ref = json.load(f)
    return auth_ref


def load_token_info():
    token_info = {}
    with open(os.path.join(local_path, 'token.json'), 'r') as f:
        token_info = json.load(f)
    return token_info


def load_user_info():
    user_info = {}
    with open(os.path.join(local_path, 'user.json'), 'r') as f:
        user_info = json.load(f)
    return user_info


def get_token(username):
    service_catalog_info = load_service_catalog()
    sc = service_catalog.ServiceCatalogV2(service_catalog_info['_catalog'])

    auth_ref_info = load_auth_ref()
    auth_ref_info['_data']['_service_catalog'] = sc
    ai = access.AccessInfoV2(auth_ref_info['_data'])

    return user.Token(auth_ref=ai)


def get_user(username, password):
    user_info = load_user_info()
    user_info['user'] = username
    token = get_token(username)
    auth_user = user.User(token=token, **user_info)
    # auth_backend = backend.KeystoneBackend()
    auth_user.backend = 'openstack_auth.backend.KeystoneBackend'
    return auth_user
    # return user.User(token=token, **user_info)

if __name__ == '__main__':
    print(get_user('admin', 'admin'))

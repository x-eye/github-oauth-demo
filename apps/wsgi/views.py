#coding=utf-8
import uuid
import requests
from bottle import get, request, redirect
from config import ClientID, ClientSecret

__author__ = 'Alexander Makarov'

github_auth_url = 'https://github.com/login/oauth/authorize'


@get('/github-oauth/connect')
def github_oauth():
    state = uuid.uuid4().get_hex()
    params = {
        'client_id': ClientID,
        'scope': 'user:email, repo',
        'state': state
    }
    r = requests.Request('GET', url=github_auth_url, params=params).prepare()
    return redirect(r.url)


@get('/github-oauth/callback')
def github_callback():
    code = request.GET.get('code')
    if not code:
        raise 404
    params = {
        'client_id': ClientID,
        'client_secret': ClientSecret,
        'code': code
    }
    headers = {'accept': 'application/json'}
    url = 'https://github.com/login/oauth/access_token'
    r = requests.post(url, params=params, headers=headers)
    if not r.ok:
        raise 404
    data = r.json()
    access_token = data['access_token']

    headers = {
        'authorization': 'token %s' % access_token
    }
    r = requests.get('https://api.github.com/user', headers=headers)
    print r.json()


if __name__ == '__main__':
    pass
'''testing for setname function'''
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_simple_success(url):
    '''Simple test to make sure the function work properly'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail2@email.com',
        'password' : 'testpassword',
        'name_first' : 'test2',
        'name_last' : 'program2',
    })

    user3 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail3@email.com',
        'password' : 'testpassword',
        'name_first' : 'test3',
        'name_last' : 'program3',
    })

    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channel1',
        'is_public' : True,
    })

    requests.post(f"{url}/admin/userpermission/change", json={
        'token' : user1.json()['token'],
        'u_id' : user2.json()['u_id'],
        'permission_id' : 1
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    details = requests.get(f"{url}/channel/details", params={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })

    assert len(details.json()['owner_members']) == 1

    requests.post(f"{url}/channel/addowner", json = {
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'u_id': user3.json()['u_id']
    })

    details2 = requests.get(f"{url}/channel/details", params={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })

    assert len(details2.json()['owner_members']) == 2

def test_not_owner(url):
    '''Accessing the change permission but not an owner'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail2@email.com',
        'password' : 'testpassword',
        'name_first' : 'test2',
        'name_last' : 'program2',
    })

    permission = requests.post(f"{url}/admin/userpermission/change", json={
        'token' : user2.json()['token'],
        'u_id' : user1.json()['u_id'],
        'permission_id' : 2
    })
    assert permission.status_code == 400

def test_invalid_target(url):
    '''Accessing the change permission but u_id is an invalid user'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })

    permission = requests.post(f"{url}/admin/userpermission/change", json={
        'token' : user1.json()['token'],
        'u_id' : 5,
        'permission_id' : 2
    })
    assert permission.status_code == 400

def test_invalid_permission_id(url):
    '''Accessing the change permission with invalid permission_id'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail2@email.com',
        'password' : 'testpassword',
        'name_first' : 'test2',
        'name_last' : 'program2',
    })    
    permission = requests.post(f"{url}/admin/userpermission/change", json={
        'token' : user1.json()['token'],
        'u_id' : user2.json()['u_id'],
        'permission_id' : 3
    })
    assert permission.status_code == 400

def test_invalid_token(url):
    '''Accessing the change permission with invalid token'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    permission = requests.post(f"{url}/admin/userpermission/change", json={
        'token' : 1234,
        'u_id' : user1.json()['u_id'],
        'permission_id' : 1
    })
    assert permission.status_code == 400

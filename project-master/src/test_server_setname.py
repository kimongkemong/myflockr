'''testing for setname function'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import pytest

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    '''generate url'''
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

def test_simple_test(url):
    '''Simple test to make sure the flask is working properly'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : 'change1',
        'name_last' : 'lastname'
    })
    profile = requests.get(f"{url}/user/profile", params={
        'token' : user1.json()['token'],
        'u_id' : user1.json()['u_id'],
    })
    assert profile.json()['user']['name_first'] == 'change1'
    assert profile.json()['user']['name_last'] == 'lastname'

def test_first_name_empty(url):
    '''change the first name to be empty'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : '',
        'name_last' : 'lastname'
    })
    assert change.status_code == 400

def test_last_name_empty(url):
    '''change the last name to be empty'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : 'change1',
        'name_last' : ''
    })
    assert change.status_code == 400

def test_both_name_empty(url):
    '''Testing to change both of the name to be empty'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : '',
        'name_last' : ''
    })
    assert change.status_code == 400

def test_long_first_name(url):
    '''Testing to change the first name longer than 50 characters'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : 'changenameinfirstnamecannotbemorethan50characters12345678910',
        'name_last' : 'lastname'
    })
    assert change.status_code == 400

def test_long_last_name(url):
    '''Testing to change the last name longer than 50 characters'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : 'firstname',
        'name_last' : 'changenameinlastnamecannotbemorethan50characters12345678910'
    })
    assert change.status_code == 400

def test_long_both_name(url):
    '''Testing to change the both last and first name longer than 50 characters'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })
    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : user1.json()['token'],
        'name_first' : 'changenameinfirstnamecannotbemorethan50characters12345678910',
        'name_last' : 'changenameinfirstnamecannotbemorethan50characters12345678910'
    })
    assert change.status_code == 400

def test_invalid_token(url):
    '''Testing the function with an invalid token'''
    requests.delete(f"{url}/clear")

    change = requests.put(f"{url}/user/profile/setname", json={
        'token' : 123456,
        'name_first' : 'change1',
        'name_last' : 'lastname'
    })
    assert change.status_code == 400

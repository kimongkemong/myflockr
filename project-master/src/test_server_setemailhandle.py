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

def test_set_handle(url):
    requests.delete(f"{url}/clear")
    # a simple to change one user handle
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    requests.put(f"{url}/user/profile/sethandle", json = {
        'token' : user1.json()['token'],
        'handle_str' : 'ariariariari'
    })
    profile = requests.get(f"{url}/user/profile", params = {
        'token' : user1.json()['token'],
        'u_id' : user1.json()['u_id'],
    })
    assert profile.status_code == 200
    #assert profile.json()['user']['handle_str'] == 'ariariariari'

def test_short_handle(url):
    r = requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    r = requests.put(f"{url}/user/profile/sethandle", json = {
        'token' : user1.json()['token'],
        'handle_str' : 'ab'
    })
    assert(r.status_code == 400)

def test_long_handle(url):
    r = requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    r = requests.put(f"{url}/user/profile/sethandle", json = {
        'token' : user1.json()['token'],
        'handle_str' : 'a'*21
    })
    assert(r.status_code == 400)

def test_same_handle(url):
    r = requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.two@gmail.com',
        'password' : 'erivan2',
        'name_first' : 'eri',
        'name_last' : 'san',
    })
    # Set handle for user1
    r = requests.put(f"{url}/user/profile/sethandle", json = {
        'token' : user1.json()['token'],
        'handle_str' : 'erivanerivan'
    })
    # Set handle for user2 to user1'handle, Expected to FAILED
    r = requests.put(f"{url}/user/profile/sethandle", json = {
        'token' : user2.json()['token'],
        'handle_str' : 'erivanerivan'
    })
    assert(r.status_code == 400)

def test_successful_setemail(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    # Set email for user1
    requests.put(f"{url}/user/profile/setemail", json = {
        'token' : user1.json()['token'],
        'email' : 'erivan.two@gmail.com'
    })
    profile = requests.get(f"{url}/user/profile", params = {
        'token' : user1.json()['token'],
        'u_id' : user1.json()['u_id'],
    })
    assert profile.json()['user']['email'] == 'erivan.two@gmail.com'
    
def test_invalid_email(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    r = requests.put(f"{url}/user/profile/setemail", json = {
        'token' : user1.json()['token'],
        'email' : 'erivane@.com'
    })
    assert(r.status_code == 400)
    
def test_same_email(url):
    r = requests.delete(f"{url}/clear")
    requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.two@gmail.com',
        'password' : 'erivan2',
        'name_first' : 'eri',
        'name_last' : 'san',
    })
    # Set email for user2 to user1's email, expected to FAILED
    r = requests.put(f"{url}/user/profile/setemail", json = {
        'token' : user2.json()['token'],
        'email' : 'erivan.one@gmail.com'
    })
    assert(r.status_code == 400)



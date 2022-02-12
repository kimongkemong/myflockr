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

def test_register_login_logout(url):
    r = requests.delete(f"{url}/clear")

    # a simple test where a user register -> logout -> login -> logout
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : r.json()['token'],
    })
    assert (r.json()['is_success'])

    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : r.json()['token'],
    })
    assert(r.json()['is_success'])


def test_email_not_registered(url):
    r = requests.delete(f"{url}/clear")
    
    # Expected to fail, since none is registered
    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
    })
    assert(r.json()['code'] == 400)

    # Sample data
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })
    
    # Expected to fail, some sample data in the storage, but login with un-registered email 
    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'unregisteredemail1@gmail.com',
        'password' : 'validpassword',
    })
    assert(r.json()['code'] == 400)

def test_invalid_password(url):
    r = requests.delete(f"{url}/clear")

    # Sample data
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })

    # LOGIN with incorrect password
    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'incorrectpassword',
    })
    assert(r.json()['code'] == 400)

def test_multiple_login(url):
    r = requests.delete(f"{url}/clear")

    # Sample data
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })

    # 1st Attempt of LOGIN
    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
    })

    #2nd attempt of LOGIN (Expected to Success)
    r = requests.post(f"{url}/auth/login", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : r.json()['token'],
    })
    assert(r.json()['is_success'])

def test_invald_email(url):
    r = requests.delete(f"{url}/clear")

    # Samples of Invalid Email
    email1 = 'invalidemailsample.com'
    password1 = 'invalidpassword1'
    email2 = '@invalidemailsample.com'
    password2 = 'password2'
    email3 = 'invalid.email@.com'
    password3 = 'password3'
    email4 = 'invalid.email@domain'
    password4 = 'password4'

    r = requests.post(f"{url}/auth/login", json = {
        'email' : email1,
        'password' : password1,
    })
    assert(r.json()['code'] == 400)

    r = requests.post(f"{url}/auth/login", json = {
        'email' : email2,
        'password' : password2,
    })
    assert(r.json()['code'] == 400)

    r = requests.post(f"{url}/auth/register", json = {
        'email' : email3,
        'password' : password3,
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })
    assert(r.json()['code'] == 400)

    r = requests.post(f"{url}/auth/register", json = {
        'email' : email4,
        'password' : password4,
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })
    assert(r.json()['code'] == 400)

def test_same_email(url):
    r = requests.delete(f"{url}/clear")

    #Registering with the same email (same data)
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'Lennon',
    })
    assert(r.json()['code'] == 400)

def test_short_password(url):
    r = requests.delete(f"{url}/clear")

    # Less than 6 letters of password
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'short',
        'name_first' : '12345',
        'name_last' : 'Lennon',
    })
    assert(r.json()['code'] == 400)
    
def test_long_first_name(url):
    r = requests.delete(f"{url}/clear")

    # Maximum length of first name -> Succesful
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'J' * 50,
        'name_last' : 'Lennon',
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : r.json()['token'],
    })
    assert(r.json()['is_success'])

    r = requests.delete(f"{url}/clear")

    # Exceeding the maximum length of first name -->Fail
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'J' * 51,
        'name_last' : 'Lennon',
    })
    assert(r.json()['code'] == 400)

def test_long_last_name(url):
    r = requests.delete(f"{url}/clear")

    # Maximum length of last name --> Success
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'L' * 50,
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : r.json()['token'],
    })
    assert(r.json()['is_success'])

    r = requests.delete(f"{url}/clear")

    # Exceeding the maximum length of last name --> Fail
    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'validemail1@gmail.com',
        'password' : 'validpassword',
        'name_first' : 'John',
        'name_last' : 'L' * 51,
    })
    assert(r.json()['code'] == 400)

def test_invalid_token_logout(url):
    # Attempting to logout using invalid token
    r = requests.delete(f"{url}/clear")

    r = requests.post(f"{url}/auth/register", json = {
        'email' : 'erivan.one@gmail.com',
        'password' : 'erivan1',
        'name_first' : 'eri',
        'name_last' : 'chan',
    })
    r = requests.post(f"{url}/auth/logout", json = {
        'token' : 12345,
    })
    assert not (r.json()['is_success'])

def test_invalid_email_reset(url):
    #raise an error if the input email was not registered
    r = requests.delete(f"{url}/clear")
    # Sample data
    email = 'validemail@gmail.com'
    r = requests.post(f"{url}/auth/passwordreset/request", json = {
        'email' : email,
    })
    assert(r.json()['code'] == 400)

def test_invalid_code_reset(url):
    #raise an error if the code was not valid
    r = requests.delete(f"{url}/clear")
    r = requests.post(f"{url}/auth/passwordreset/reset", json = {
        'reset_code' : 'DUMMYCODE',
        'new_password' : 'DUMMYPASSWORD'
    })
    assert(r.json()['code'] == 400)
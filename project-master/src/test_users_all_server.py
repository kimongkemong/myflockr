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


#make sure that url works well
def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}


#If the token is invalid, then raise an AccessError
def test_ua_empty(url):

    requests.delete(f"{url}/clear")

    res = requests.get(f"{url}/users/all", params = {'token':1})

    assert res.status_code == 400

#If the token is valid, then all the user profiles will be returned
def test_ua_valid(url):

    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    requests.post(f"{url}/auth/register", json = {
        'email':'suarez@atmadrid.com', 
        'password':'lovemessi123', 
        'name_first':'Luis', 
        'name_last':'Suarez'
    })    

    requests.post(f"{url}/auth/register", json = {
        'email':'havertz@chelsea.com', 
        'password':'german098', 
        'name_first':'Kai', 
        'name_last':'Havertz'
    })  

    requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    users_info = requests.get(f"{url}/users/all", params = {
        'token':data1.json()['token']
    })  

    assert users_info.json() == {
        'users': [{'u_id': 1, 
                   'email': 'messi@barca.com', 
                   'name_first': 'Lionel', 
                   'name_last': 'Messi', 
                   'handle_str': 'LionelMessi','profile_img_url' : "",}, 

                  {'u_id': 2, 
                   'email': 'ronaldo@juventus.com', 
                   'name_first': 'Cristiano', 
                   'name_last': 'Ronaldo', 
                   'handle_str': 'CristianoRonaldo','profile_img_url' : "",}, 

                  {'u_id': 3, 
                   'email': 'suarez@atmadrid.com', 
                   'name_first': 'Luis', 
                   'name_last': 'Suarez', 
                   'handle_str': 'LuisSuarez','profile_img_url' : "",}, 

                  {'u_id': 4, 
                   'email': 'havertz@chelsea.com', 
                   'name_first': 'Kai', 
                   'name_last': 'Havertz', 
                   'handle_str': 'KaiHavertz','profile_img_url' : "",}, 
                   
                  {'u_id': 5, 
                   'email': 'bsilva@mancity.com', 
                   'name_first': 'Bernado', 
                   'name_last': 'Silva', 
                   'handle_str': 'BernadoSilva','profile_img_url' : "",}]
    }

                                                    